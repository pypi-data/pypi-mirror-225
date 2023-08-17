import io
import re
import pandas as pd
from typing import List,Dict,Optional,Union,Tuple
import poplib
poplib._MAXLINE=20480
import smtplib
from datetime import datetime
import warnings

from email.message import EmailMessage
from email.parser import Parser
from email import policy

from .constant import MailHeaderData,NetValueData
from .utils import decode_str,parse_mailaddr


# 定义一个警告格式，只包含警告的消息
simple_format = "%(message)s"
warnings.formatwarning = lambda message, category, filename, lineno, line=None: \
    simple_format % {"message": message}

class MailClient:
    def __init__(
            self,
            username:str,
            password:str,
            server_addr:str = "mail.gyzq.com.cn",
            smtp_server_port:int = 465,
            pop3_server_port:int = 110,
        ) -> None:
        
        receiver = poplib.POP3(server_addr,pop3_server_port)
        receiver.user(username)
        receiver.pass_(password)
        self.receiver = receiver


        sender = smtplib.SMTP_SSL(server_addr, smtp_server_port)
        sender.login(username,password)
        self.sender = sender

    @property
    def mail_num(self):
        """邮箱现有邮件数"""
        mail_num, _ = self.receiver.stat()
        return mail_num

    def _retrive_mail(self,mailindex,save=False)->EmailMessage:
        """
        收取指定邮件全文:
        args:
            mailindex: 收取邮件的顺位(最早的一封为1) 注意：如有邮件删除,顺位会变!
        output:
            msg:EmailMessage
        """
        _, lines, _ = self.receiver.retr(mailindex)
        msg_content = b'\r\n'.join(lines).decode('gbk')
        msg = Parser(policy=policy.default).parsestr(msg_content)
        return msg
        
    def _parse(self,mesg:EmailMessage)->Tuple[MailHeaderData,str,Optional[Dict[str,bytes]]]:
        """
        解析邮件内容：
        args:
            mesg:EmailMessage对象
        output:
            tuple:
                邮件的标题信息:MailHeaderData
                邮件正文信息:str
                邮件附件:Dict:
                            key:filename
                            value:byte文件
        """
        required_attrs = ['From','To',"Date","Subject"]
        if not set(required_attrs).issubset(mesg.keys()):
            warnings.warn(f"{mesg['Subject']}邮件头信息缺失{set(required_attrs).difference(mesg.keys())}字段\n")
        
        date_regex = r".+([0-9]{2}:){2}[0-9]{2}"

        sender_name,sender_addr= parse_mailaddr(mesg["From"])
        receriver_name,receriver_addr= parse_mailaddr(mesg["TO"])
        cc_name,cc_addr= parse_mailaddr(mesg["cc"])

        mailheader = MailHeaderData(
            Date=datetime.strptime(re.match(date_regex,mesg["date"]).group(),"%a, %d %b %Y %H:%M:%S"),
            sender_name=sender_name,
            sender_addr = sender_addr,
            receriver_name= receriver_name,
            receriver_addr = receriver_addr,
            cc_name = cc_name,
            cc_addr = cc_addr,
            Subject = decode_str(mesg["Subject"]),
        )
        # print(mailheader)
        mailcontent = mesg.get_body(preferencelist=["html","plain"])
        if mailcontent:
            # print(mailheader.Subject)
            # print(mailcontent.get_content_type())
            mailcontent = mailcontent.get_content()

        attachments = {}
        for mesg_attachment in mesg.iter_attachments():
            if mesg_attachment.is_attachment():
                filename = mesg_attachment.get_filename()
                data = mesg_attachment.get_payload(decode=True)
                attachments[filename] = data
        
        return mailheader,mailcontent,attachments
    
    def get_mail_header(
            self,
            mail_indexex:List[int]=None,
            lookin_depth=10,
            df:bool=False
        )->Union[Dict[int,MailHeaderData],pd.DataFrame]:
        """
        收取邮箱邮件标题

        args:
            mail_indexex:指定的邮件索引
            lookin_depth:从最新一份向前回溯的邮件数,None为全量收取
        return:
            Dict of MailHeaderData,keyed by mailindex;or Dataframe
        """
        mail_num = self.mail_num

        if not mail_indexex:
            if lookin_depth is None:
                lookin_depth=mail_num
            mail_indexex = range(mail_num-lookin_depth+1,mail_num+1)
        
        if isinstance(mail_indexex,int):
            mail_indexex = [mail_indexex]
        
        mailheaders = {}
        for mail_index in mail_indexex:
            _, lines, _ = self.receiver.top(mail_index, 0)
            msg_content = b'\r\n'.join(lines).decode('gbk')
            msg = Parser(policy=policy.default).parsestr(msg_content)
            mailheader = self._parse(msg)[0]
            mailheaders[mail_index] = mailheader
            
        if df:
            mailheaders = pd.DataFrame(mailheaders.values(),index=mailheaders.keys())
            
        return mailheaders

    
    def parse_source(self,mailheaders:Dict[int,MailHeaderData])->Dict[str,List[int]]:
        """
        通过邮件头区分邮件类别,目前支持区分中信("CITIC"),招商("CMS"),中泰("ZTS")的净值邮件
        args:
            mailheaders:dict[mail_index,MailHeaderData]
        output:
            Dict:{category,mail_index}
        """
        mail_category = {
            "CITIC":[],
            "CMS":[],
            "ZTS":[],
        }

        for mail_index,mailheader in mailheaders.items():
            if ("Auto-Disclosure@citics.com" in mailheader.sender_addr) and ("基金净值表现估算" in mailheader.Subject):
                mail_category["CITIC"].append(mail_index)
            if ("yywbfa@cmschina.com.cn" in mailheader.sender_addr) and ("净值表" in mailheader.Subject):
                mail_category["CMS"].append(mail_index)
            if ("fundservice@zts.com.cn") in mailheader.sender_addr and ("净值信息发送" in mailheader.Subject):
                mail_category["ZTS"].append(mail_index)

        return mail_category


    def _parse_citic_mails(self,mesg:EmailMessage)->NetValueData:
        """
        解析中信中证的净值邮件
        args:
            mesg:需要解析的邮件
        output:
            NetValueData:解析后的净值数据
        """
        mailheader,mailcontent,attachments = self._parse(mesg)
        # 从标题解析
        subject_regex = r"([A-Z0-9]+)_([^_]+)_(.+)$"
        match_result = re.search(subject_regex,mailheader.Subject)
        try:
            prodcode = match_result.group(1)
            # print(match_result.group(1))
            # print(match_result.group(2))
            # print(match_result.group(3))
            prodname = match_result.group(2)
            date = datetime.strptime(match_result.group(3),"%Y-%m-%d")
            
        except:
            print("解析有误: "+mailheader.Subject)
    
        # 从内容解析
        index_regex = r">([^<]+)</th"
        content_keys = re.findall(index_regex,mailcontent)
        values_regex = r">([^<]+)</td"
        content_values = re.findall(values_regex,mailcontent)
        content = dict(zip(content_keys,content_values))

        netvalue = float(content.get("单位净值"))
        cum_netvalue = float(content.get("累计单位净值"))
        netasset = content.get("资产净值")
        if isinstance(netasset,str):
            netasset = netasset.replace(",", "")
            netasset = float(netasset)
        
        if netasset is not None:
            shares = netasset/netvalue
        else:
            shares = None
        
        nvdata = NetValueData(
            date=date,
            prodcode=prodcode,
            prodname=prodname,
            netvalue=netvalue,
            cum_netvalue=cum_netvalue,
            netasset = netasset,
            shares=shares
        )
        return nvdata

    def _parse_cms_mails(self,mesg:EmailMessage)->NetValueData:
        """
        解析招商的净值邮件
        args:
            mesg:需要解析的邮件
        output:
            NetValueData:解析后的净值数据
        """
        mailheader,mailcontent,attachments = self._parse(mesg)
        # 从内容解析
        regex=r'5;">([^<]+)'
        values = re.findall(regex,mailcontent)[1:]
        if len(values)==7:
            date,prodcode,prodname,netasset,shares,netvalue,cum_netvalue = values
        elif len(values)==5:
            date,prodcode,prodname,netvalue,cum_netvalue = values
            netasset = None
            shares = None
        else:
            raise ValueError(f"{mailheader.Subject}格式不符合已有形式")
        
        netvalue = float(netvalue)
        cum_netvalue = float(cum_netvalue)
        if isinstance(netasset,str):
            netasset = netasset.replace(",", "")
            netasset = float(netasset)
        if isinstance(shares,str):
            shares = shares.replace(",", "")
            shares = float(shares)

        date = datetime.strptime(date,"%Y年%m月%d日")

        nvdata = NetValueData(
            date=date,
            prodcode=prodcode,
            prodname=prodname,
            netvalue=netvalue,
            cum_netvalue=cum_netvalue,
            netasset = netasset,
            shares = shares,
        )
        return nvdata
    
    def _parse_zts_mails(self,mesg:EmailMessage)->List[NetValueData]:
        """
        解析中泰的净值邮件
        args:
            mesg:需要解析的邮件
        output:
            NetValueData:解析后的净值数据
        """

        mailheader,mailcontent,attachments = self._parse(mesg)
        nv_data = []
        #从附件解析邮件
        for filename,filedata in attachments.items():
            with io.BytesIO(filedata) as file_stream:
                df = pd.read_excel(filedata)[0:5].set_index("基金净值信息").T.drop_duplicates(" 基金代码：")
                for row in df.itertuples():
                    nv_data.append(NetValueData(
                        date=datetime.strptime(row[3],"%Y-%m-%d"),
                        prodcode=row[1],
                        prodname=row[2],
                        netvalue=float(row[4]),
                        cum_netvalue=float(row[5]),
                    ))
        return nv_data


    def parse_mails(
        self,
        mailheaders:Dict[int,MailHeaderData],
    )->List[NetValueData]:
        """
        解析邮箱净值:
            args:
                mail_indexex,需要解析的邮件索引
            output:
                List[NetValueData]:净值数据列表
        """
        mail_category = self.parse_source(mailheaders)

        nv_list = []
        for source,mail_indexex in mail_category.items():
            for mail_index in mail_indexex:
                msg = self._retrive_mail(mail_index)
                if source == "CITIC":
                    nv = self._parse_citic_mails(msg)
                elif source == "CMS":
                    nv = self._parse_cms_mails(msg)
                elif source == "ZTS":
                    nv = self._parse_zts_mails(msg)
                else:
                    continue
                
                if isinstance(nv,NetValueData):
                    nv = [nv]
                
                for nv_ in nv:
                    if nv_ not in nv_list:
                        nv_list.append(nv_)
        return nv_list

    
    def save_netvalue(
            self,
            new_net_values:List[NetValueData],
            local_file:str=None):
        """
        更新本地的净值解析文件
        args:
            new_net_values:新解析的净值数据
            save_file:本地储存文件路径,如有数据则更新,如没有则创建
        output:
            None
        """
        if len(new_net_values)>0:
            new_net_values = pd.DataFrame(new_net_values).set_index(["date","prodcode"])
            try:
                local_net_values = pd.read_excel(local_file,index_col=[0,1])
                net_values = local_net_values.combine_first(new_net_values)
                net_values = net_values.sort_index(ascending=[False,True])
                net_values.to_excel(local_file)
            except:
                new_net_values.sort_index(ascending=[False,True]).to_excel(local_file)