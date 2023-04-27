# 参考连接：https://www.jianshu.com/p/c2809c56fff1
# 代码思路：
# 1. 下载知乎专栏文章存入html
# 2. 将所有html转换为md
# 3. 正则提取markdown中的图片链接
# 4. 下载图片至本地
# 5. 上传图片至码云图床
# 6. 使用新图片链接替换原来的图片链接

import requests
from requests_toolbelt import MultipartEncoder
import json 
import html2text as ht
import os
import re
import base64
from urllib.parse import quote
import time


cookies="_xsrf=rg4Dp0wF3EyG4WKiifldrEZIOMiVByB3; _zap=09ed752b-cb5b-4b71-b56b-b79edf7357a3; d_c0=AHDW0Q09PhaPTp6aFrOciFDs2ffpllnB0dA=|1674913876; __snaker__id=xUsslaaS6qHmFONj; captcha_session_v2=2|1:0|10:1674913877|18:captcha_session_v2|88:NHZ3ZW0zNXRJbjU4Z3B3NEFXVzJpa1RyZzQwbzJ6NlYvQmJ1L2NCaExmR25FTlJsOWUyVzRUK0tXR0lOYzJXaA==|44b13e113e9b43afbefc8b9eac19ce443c892f9cc81e8896b041a9b03ffb7998; gdxidpyhxdE=46qtIQCTR9jVXkGkgCQQ/EXX9O0kwk+vsI8PxiBg8aL0DsAXlO8oc1z/1tYZcJ7USEzdpJ+IXxSeI5LsMyLSHPcYAB+wluqTWf9PgWUMbpv3\78hU5OVUYmlIUhN8aU89D7J/KmDVyzXQDfGK2oxVKcOTa6voZgzNDKqkD2epUESE1Bm:1674914777807; YD00517437729195:WM_NI=OnoNz4ighCPxTrpfdXhw72Ur9cn8GeCXhpO3PG8keq4hQ/22w/Ic/j0B/gcN8fbrG4hTo4cmiOwtMui2ntIullYdx7pp4dRfGeDMYYjWzIW0QiqePJEtajOlF3gLkXAuVXI=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6eed4f95cf4b1e1b8cf7dafeb8fb3c55b979e9bacd547f5aa9f9acb6f9c9bfe84f22af0fea7c3b92a8db2a1aff940abb9a8a4d37498aec087e754aca9f9d3d87afbbda2d9c66f8188a891ce399499f88ce87bf8b89fd0b13ab5f18784ae62f49ee188e246fcbaae93c640ac8ca1d5e267ab91b995d07fabeea295cc7fb0b49785fb3db4b0fc85d16e85bb8caedc53aa89b6aad63c93b7bf86d34287acaf8bce6886eda9adea5483ab9ab9cc37e2a3; YD00517437729195:WM_TID=SbSIFWUaOFpAEAQBFVbUNr6EmWfSAyJp; captcha_ticket_v2=2|1:0|10:1674913901|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfOEd0LlYuSGkydWFvV3pIaVBlTHJpZVdmSmpDRklzOElGeENid3dNYjQwbWNTSEZpby5EQ1R4dDBBdEM1bnRsci5OeENFeWRXOE5tcENkWHlVakxyT1lyY0kwcDVhakU0MHNnamVTOGxCS3E2cWM4ZUl4YjVnNHRCV2ZSN2doeGlpT3N6MVNGR1cuZ3k2ZFRNZnVwR2R6R0FWeWdWbHRNRi1FX3BnLm1ndlRqei4xX3IuUE9wWV94ZFhPZ0pBMnJxV1VCRGJYT29sRnhlWHFqVmRNV3dHYjA0S3ZSZWN3Zmd1QVpxaTBTZ3VhazFrRW9SSUtwS2cxOEZRei5oSG1lRXVURE9ETW5EeU01enByblRObkRPTC56RElGVkV1QURJNWhWcDRkVHJRcWVtSXdnV0dNNjVONjZUNzZHWThDTlBUOG9BcW1DQ3hHcTF1UnJ5SmtnelBqSElvSUVjNXR0d3ZuLnpYYWZCMkQtVExtUkd3c3RHa1VjOEpWaHZlcE8uRVAuZnZscERuLU5WeGthZGhBckZzNndfT3pySzAwbVc0Y1R3UHpDdERDQU9FV2w2eWx3MjZPX2t6Snh2LXRsSHlsUVhhc0ZGUmV1azFqWTlrZEw3NWFSTGFPSi4xeEIxNGg4TmNMUjhlek5nNzdheEw2enFwZjZaT3pjMyJ9|2c79073d4ab6f5f654c1b0831b832262224d25827d3676e9be4a98050e19e169; q_c1=4611740cea3f4c4db2b597d05b5f04e4|1674913901000|1674913901000; z_c0=2|1:0|10:1674914018|4:z_c0|92:Mi4xSGxsWkFnQUFBQUFBY05iUkRUMC1GaVlBQUFCZ0FsVk5iWGJDWkFDQkRCNEctRm5xVWZUTXV3b0Z0R3FWc3B0WjRn|4905a3584cfb3144d3ac41a894403040c6e2aa45ecc685ad7bfa2eb8b624e8f5; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1675581436,1675957394,1676166884,1676287683; BAIDU_SSP_lcr=https://www.baidu.com/link?url=dabnjyuirZQXNbsUEoIug4RW4tSuPReUunNCawo_b5MwdkSiQWhFvjrfvf6vUa5xcU2N-MTrGoltN6qsZUwmAq&wd=&eqid=a1ffcfe20006d3150000000463ea1eb4; SL_G_WPT_TO=zh; arialoadData=false; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; SESSIONID=hooeatcBx881WTp0PRJnnY44Hs96xeBsQ9WiHe7eYr9; JOID=VlgVBULcGR5BETZVLt4QzW8WCWI8sHZ3K31GNmqpJSZ2SW8hHhwB_SAYMlMnvBvYURtDOGNEyu4yVFHTjbx5KfY=; osd=UFgXC0zaGRxPHzBVLNAey28UB2w6sHR5JXtGNGSnIyZ0R2EnHh4P8yYYMF0puhvaXxVFOGFKxOgyVl_di7x7J_g=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1676288962; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1676292617|1676287681"
headers={   # 设置requests要用到的header
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# 下载知乎专栏文章存入html
def downloadZhuanLanToLocalHtml(zhuanLan,htmlSavePath):
    """
    下载知乎专栏文章存入html
    :param zhuanLan: 专栏地址  https://www.zhihu.com/column/c_1341718720926887936  地址是c_1341718720926887936
    :htmlSavePath: html文件存放路径
    """
    # 获取总的文章数量
    urlIndex=f"https://www.zhihu.com/api/v4/columns/{zhuanLan}/items"
    res=requests.get(urlIndex,headers=headers)
    # 知乎比较友好，返回的是json
    totals=json.loads(res.text)["paging"]["totals"]
    totalPage=totals//100+1  # 获取总页数
    for i in range(totalPage):
        # limit最大是100,超过会报错
        urlpage = 'https://www.zhihu.com/api/v4/columns/{}/items?limit={}&offset={}'.format(zhuanLan, 100, 100*i)
        respage = requests.get(urlpage, headers=headers)
        data=json.loads(respage.content)['data']
        for article in data:
            title=article["title"]
            content=article["content"]
            # 替换标题中的特殊符号，不然创建文件会报错
            with open(f'{htmlSavePath}\\{title.replace("?","").replace("？","")}.html',"w",encoding="utf-8") as f:
                f.write(content)
    print("下载完成")



      
def convertHtml2Markdow(htmlSavePath,mdSavePath):
    '''
    将所有html转换为md
    : htmlSavePath: 存放html文件的文件夹路径
    : mdSavePath:  存放markdown文件的文件夹路径
    '''
    for file in os.listdir(htmlSavePath):
        # 获取文件名称
        filename=os.path.basename(file).split(".")[0]
        text_maker = ht.HTML2Text()
        # 读取html格式文件
        with open(htmlSavePath+"/"+file, 'r', encoding='UTF-8') as f:
            htmlpage = f.read()
        # 处理html格式文件中的内容
        text = text_maker.handle(htmlpage)
        # 写入处理后的内容
        with open(mdSavePath+"/"+filename+".md", 'w', encoding='UTF-8') as f:
            f.write(text)


def lambdaToGetMarkdownPicturePosition(content):
    """
    从markdownd代码中提取图片链接
    :param content: 
    :return: 
    """
    pattern = re.compile(r"!\[.*?\]\([https|http].*?source=.*?\)")
    resultList = pattern.finditer(content)
    urlList = []
    for item in resultList:
        curStr = item.group()
        curStr = curStr.split('(')[1]
        curStr = curStr.strip(')')
        urlList.append(curStr)
        print(curStr)
    return urlList


'''
<img src="https://picx.zhimg.com/v2-4db6922545ab7783cb352cf6e934eea5_720w.jpg?source=d16d100b" data-caption="" data-size="normal" data-rawwidth="1135" data-rawheight="416" class="origin_image zh-lightbox-thumb" width="1135" data-original="https://pica.zhimg.com/v2-4db6922545ab7783cb352cf6e934eea5_720w.jpg?source=d16d100b">
'''
def lambdaToGetHtmlPicturePosition(content):
    """
    从html代码中提取图片链接
    :param content: 
    :return: 
    """
    pattern = re.compile(r"<img.*?>")
    resultList = pattern.finditer(content)
    urlList = []
    for item in resultList:
        searchObject = re.search(r'src=".*?"', item.group())
        curStr = searchObject.group()
        curStr = curStr.split('"')[1]
        curStr = curStr.strip('"')
        urlList.append(curStr)
    return urlList



def downloadPic(urls,picSavePath):
    '''
    下载图片至本地
    : urls: 图片路径
    ：picSavePath: 本地存放图片的文件夹
    '''
    picMap={}
    for url in urls:
        res=requests.get(url)
        if res.status_code==200:
            savePicName=url.split("/")[-1]
            with open(f"{picSavePath}/{savePicName.split('?')[0]}","wb") as f:
                f.write(res.content)
            picMap[url]=f"{picSavePath}/{savePicName.split('?')[0]}"
        else:
            print("图片下载失败")
    return picMap







'''
https://gitee.com/api/v5/swagger#/postV5ReposOwnerRepoContentsPath

https://toolbelt.readthedocs.io/en/latest/user.html#multipart-form-data-encoder
'''

def uploadPicToGitee(picFullPath,access_token="76be323fb052abe0171d301b3ac4986f",owner="teisyogun",repo="images",branch="master",giteeRepoSavePath="img"):
    '''
    上传文件到gitee
    :picFullPath: 本地图片路径
    :giteeRepoSavePath: gitee仓库中文件存放路径
    '''
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'user_locale=zh-CN; oschina_new_user=false; remote_way=http; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; feature_log_id=9; slide_id=9; user_return_to_0=https%3A%2F%2Fgitee.com%2Foauth%2Fauthorize%3Fclient_id%3D8ac7a94ff19ddb4b9d267d525c048e2845f589cf3b1e8d09ef2568ca63f74603%26redirect_uri%3Dhttps%253A%252F%252Fgitee.com%252Fapi%252Fv5%252Fswagger%26response_type%3Dcode; tz=Asia%2FShanghai; Hm_lvt_24f17767262929947cc3631f99bfd274=1675086289,1675263054,1675527132,1676308702; remember_user_token=BAhbCFsGaQNecAhJIiIkMmEkMTAkZnUxQWl0WEhYSDlqMFVIWlY2ZU5yTwY6BkVUSSIXMTY3NjMwODcwNS4yMTgxMTI1BjsARg%3D%3D--2a33b1da94debc81eddf264ee84a239afdb85d09; gitee_user=true; access_token=76be323fb052abe0171d301b3ac4986f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22553054%22%2C%22first_id%22%3A%221864bc8e3e8182e-06ee24a96708378-26021051-2073600-1864bc8e3e91658%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg1Zjk4MGMxNDkxMzQwLTAyYzhiOWZhM2RhYTJjYy0yNjAyMTA1MS0yMDczNjAwLTE4NWY5ODBjMTRhMTdmYSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjU1MzA1NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22553054%22%7D%2C%22%24device_id%22%3A%22185f980c1491340-02c8b9fa3daa2cc-26021051-2073600-185f980c14a17fa%22%7D; Hm_lpvt_24f17767262929947cc3631f99bfd274=1676308761; gitee-session-n=OWI0c1FkUENJYkdKa2dUb2Q5OGl0djJzbmE5QVNRbkN4c2RxY1lKVWhKYWllcTJkS1hYc2ZiSS9CN3c4aUtLYmNnaWFTV011bnNNem40aW11dWVWOXNFQXIxN0xHUUJvS3REM2t6a3FGRlduQkluL1NIazZPSnhIQ2tuQkpEQ0FLeXZHaEU0Sit3NkpBckxwTjAreFRQd2F4U21QbUJ1VnRieHkzclBscVpRTkl6UUFlOEpITUlTd21iaHA2TzliSU9QMmNTdFowdTdOWXFtSjhEa1hEbzNLTmRCUzh3ZnFSdEZ5RE9GVmplQTBGK0Uva2lSMlV5UGxJTW9zQ2R5M0NUaVFaL3BUbmFRd2p4ZTRRb3hWMW5POGlJSk9NNzk5ODNVejJRWGRycjM2NWdqczVPUStjaldlbWdKbWUwOG5ETk9aZjB0amkyY0pSQW9tL2JOOWVxYTBNaElmOTRxc1FrSnlaTjh4ellnaTJFQllqWE5keVV3N0Q1NjR3M1o0RjFaN2QxTkQvMGR3Njg2SkxZMi9EUTJiVnJKL1hiZ3gyUnk4ZmsrL05kSEhQSGZaNmpDRXNQY2FtME80aTE1STk3bmk4ckdKRjhrY2tZSk51eWUrM3BHMHhtaTV1ZmFhM2FZYXo0aG5ySTVnZ3NQV2hrY05wWGRPSE1NeHMxWllXamdyTmsyanNGWnQ5dTd4dmdnUisxdWFBSHpYMmIrRy9GVTA1Qk16NGpyT2lDNDY3dWFiYVNoNkdKTjNMK2pMTEhKT3JPTjVGVjZZalpzakU3Nmc0eUlldHNHM05pSTZqM0QvWDRDUnVhdWVNT1p0YTk2bEtCMjZJd2lSQ21DaC0tMDFoZTQvMnNVMGNMQjVyUjNXK00wQT09--5c00eeb664c067b6ba96b9080c4b473eb12685e8',
        'Origin': 'https://gitee.com',
        'Referer': 'https://gitee.com/api/v5/swagger',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # 将图片进行bas4编码
    with open(picFullPath,"rb") as f:
        content=base64.b64encode(f.read())
    
    picDir=os.path.dirname(os.path.abspath(picFullPath))
    # 切换目录
    os.chdir(picDir)
    picName=os.path.basename(picFullPath)
    data = {
        'access_token': access_token,
        'content': content,
        'message': f'upload-{picName}',
        'branch': branch,
    }

    # 上传文件需要处理data 
    data=MultipartEncoder(fields=data)
    headers['Content-Type']=data.content_type

    res = requests.post(f'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{giteeRepoSavePath}/{picName}', headers=headers, data=data,verify=False)
    if res.status_code==201 or res.text=='{"message":"A file with this name already exists"}':
        imgUrl=f'https://gitee.com/{owner}/{repo}/raw/{branch}/{giteeRepoSavePath}/{quote(picName)}'
        return imgUrl
    return None

# https://www.jianshu.com/p/b8530e554782
# https://www.dandelioncloud.cn/article/details/1487706447181107201







if __name__=="__main__":
    zhuanLan="c_1341718720926887936"
    htmlSavePath=r"C:\Users\teisyogun\Desktop\脚本\python_learn\test\test"
    mdSavePath=r"C:\Users\teisyogun\Desktop\脚本\python_learn\test\test-md"
    # downloadZhuanLanToLocalHtml(zhuanLan,htmlSavePath)
    # convertHtml2Markdow(htmlSavePath,mdSavePath)

     
    mdSavePath1=r"C:\Users\teisyogun\Desktop\脚本\python_learn\test\test-md\test3"



    picSavePath=r"C:\Users\teisyogun\Desktop\脚本\python_learn\test\test-pic"
    for root,dirs,files in os.walk(mdSavePath1):
        for filename in files:
            mdFullPath=os.path.join(root,filename)
            mdBakFullPath=os.path.join(root,filename.replace(".md","-bak.md"))
            with open(mdFullPath,"r+",encoding="utf-8") as f,open(mdBakFullPath,"w",encoding="utf-8") as wf:
                print(mdFullPath)
                mdContent="".join(f.readlines())
                urlList=lambdaToGetMarkdownPicturePosition(mdContent)
                if len(urlList)!=0:
                    picMap=downloadPic(urlList,picSavePath)
                    print(picMap)
                    if bool(picMap):
                        for picUrl in picMap:
                            imgUrl=uploadPicToGitee(picMap[picUrl])
                            
                            print(imgUrl)
                            if imgUrl is not None:
                                mdContent=mdContent.replace(picUrl,imgUrl)
                            else:
                                print(f"文件：{filename}中{picMap[picUrl]}替换失败")
                        wf.write(mdContent)
                        print(f"{filename}+===替换完成")
                else:
                    wf.write(mdContent)
                        



                
                

    