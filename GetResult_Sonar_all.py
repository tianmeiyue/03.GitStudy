import requests    
import urllib
import json
from requests.auth import HTTPBasicAuth


server="http://localhost:9000"
##headers = {'Content-Type': 'application/x-www-form-urlencoded'}
##Auth = HTTPBasicAuth('admin','admin')
##user_password = {"login":"admin", "password": "admin"}
session = requests.session()

def Login():
    url = server + "/api/authentication/login"
    data = user_password
    response_url_get = session.post(url,headers = headers, data=urllib.parse.urlencode(data))
##    token = response_url_get.cookies.get_dict()['XSRF-TOKEN']   获取token
##    print(response_url_get.cookies)
    return response_url_get.cookies


def GetComponents():  ##获取项目信息
    url = server + "/api/components/search_projects?f=analysisDate%2CleakPeriodDate"
    response_url_get = session.get(url=url)  ## 网页是公开的，暂时不需要Cookies和Login 
##    print(response_url_get.content)
    return json.loads(response_url_get.content)


def GetQualityGates():    ##获取质量门限
    url = server + "/api/qualitygates/project_status?projectKey=QisiDialer"
    response_url_get = session.get(url=url) 
##    print(response_url_get.content)
    return json.loads(response_url_get.content)


##获取CodeSmells信息  可选"sqale_index","duplicated_lines_density","ncloc","coverage",
def GetCodeSmells(component,metrics = ["bugs","vulnerabilities","code_smells"],ps="1000",fromdate="2023-06-12"):  ##过滤信息的话，需要增加一些参数，参考 http://localhost:9000/web_api，增加参数时用fromdate="2023-06-12"这种类型
    params = {"component":",".join(component),"metrics":",".join(metrics),"ps":ps, "from" : fromdate}             ##对于URL来说，？后面跟着参数，参数形式为XXX=XXX，各参数之间用&连接
    url = server + "/api/measures/search_history?" + urllib.parse.urlencode(params)
    response_url_get = session.get(url=url)
##    print(response_url_get.content)
    return json.loads(response_url_get.content)


##    "http://localhost:9000/
##    api/measures/search_history?
##    component=QisiDialer
##    &metrics=bugs%2Cvulnerabilities%2Csqale_index%2Cduplicated_lines_density%2Cncloc%2Ccoverage%2Ccode_smells
##    &ps=1000


def GetMeasures(projectKeys, metricKeys = ["bugs", "vulnerabilities", "codesmells"]):    ##获取度量数据
    params = {"projectKeys":",".join(projectKeys ), "metricKeys": ",".join(metricKeys)}
    url = server + "/api/measures/search?" + urllib.parse.urlencode(params)
    
    response_url_get = session.get(url=url)
##    print(response_url_get.content)
    return json.loads(response_url_get.content)


##def GetDetails(params = {"componentKeys":"QisiDialer", "s":"FILE_LINE", "resolved":"false", "types":"BUG", "ps":"100",
##              "organization":"default-organization","facets":"severities,types", "additionalFields":"_all"}):    ##获取detail

def GetDetails(componentKeys, resolved, types,facets):
    params = {"componentKeys":",".join(componentKeys if isinstance(componentKeys,list) else [componentKeys]),
              "resolved":",".join(resolved if isinstance(resolved,list) else [resolved]),
              "types":",".join(types if isinstance(types,list) else [types]),
              "facets":",".join(facets if isinstance(facets,list) else [facets])}
    url = server + "/api/issues/search?" + urllib.parse.urlencode(params)
    response_url_get = session.get(url)
##    print(response_url_get.content)
    return json.loads(response_url_get.content)



if __name__ == '__main__':    
    cookies = Login()
    
    GetComponents()
    GetQualityGates()
    GetMeasures(['QisiDialer'])
    GetCodeSmells(['QisiDialer'])

##  url_details = url_details_base + urllib.parse.urlencode(url_details_params)  ##urlencode会对%等进行转义，所以参数中包含%2c的需要在替换为‘，’
    GetDetails( componentKeys=["QisiDialer"], resolved=["false"], types=["BUG"],
              facets=["severities,types"])




##     def GetDetails针对某一故障，输出以下信息
##{
##		"key": "AYiumCkqcOmDF53nowQP",
##		"rule": "squid:S3077",
##		"severity": "MINOR",
##		"component": "QisiDialer:app/src/main/java/ltd/qisi/dialer/TelApplication.java",
##		"project": "QisiDialer",
##		"line": 67,
##		"hash": "dc149520f315267537725a41bb8c6750",
##		"textRange": {
##			"startLine": 67,
##			"endLine": 67,
##			"startOffset": 19,
##			"endOffset": 42
##		},
##		"flows": [],
##		"status": "OPEN",
##		"message": "Remove the \\"
##		volatile\\ " keyword from this field.",
##		"effort": "20min",
##		"debt": "20min",
##		"tags": ["cert", "multi-threading"],
##		"transitions": [],
##		"actions": [],
##		"comments": [],
##		"creationDate": "2023-06-12T15:51:46+0800",
##		"updateDate": "2023-06-12T15:51:46+0800",
##		"type": "BUG",
##		"organization": "default-organization",
##		"fromHotspot": false}
