import requests
import urllib
import json

server = 'http://localhost:9000/'

def GetCodePaths_OnePage(url_base,p,ps,lst):
    url = url_base + f'&p={p}'
    response_path_get = requests.get(url)
    obj = json.loads(response_path_get.content)
    lst.extend(each["path"] for each in obj["components"])
    total = obj["paging"]["total"]
    
    return p * ps <= total


def GetSmellsPath(component):
    pathlst = []
    p=1
    ps=100
    url_base = server + f'''api/measures/component_tree?additionalFields=metrics
&ps={ps}&asc=false&metricSort=new_code_smells&s=metricPeriod&metricSortFilter=withMeasuresOnly
&metricPeriodSort=1&component={component}&metricKeys=new_code_smells&strategy=leaves'''
    while GetCodePaths_OnePage(url_base,p,ps,pathlst):
        p = p+1
        
    return pathlst



def GetCodeSmells_OnePage(p,ps,url_base,lst,typ):
    url = url_base + f'&p={p}'
    response_smell_get = requests.get(url)
    obj = json.loads(response_smell_get.content)
    total = obj["total"]
    issues = obj["issues"]
    lst.extend([each["line"] if "line" in each else "全文件" for each in issues if each["type"] == f"{typ}"])

    return p*ps <= total
    

def GetCodeSmells(resolved,componentKeys,typ):

    pathlst = GetSmellsPath(componentKeys)
    smellslst = []
    for each in pathlst:
        p = 1
        ps = 50
        url_base = server + f'api/issues/search?additionalFields=_all&resolved={resolved}&componentKeys={componentKeys}:' + each + f'&s=FILE_LINE&ps={ps}'
        while GetCodeSmells_OnePage(p,ps,url_base,smellslst,typ):
            p = p+1
    
    return smellslst
        



if __name__ == '__main__':

    resolved = "false"
    componentKeys = "QisiDialer"
    typ = "CODE_SMELL"
    GetCodeSmells(resolved,componentKeys,typ)


##            smellslst.extend([each["line"] if "line" in each else "全文件" for each in issues if each["type"] == f"{typ}"])      
##        for each in issues:
##            if each["type"] == "CODE_SMELL" and "line" in each:
##                smellslst.append(each["line"])
##            elif each["type"] == "CODE_SMELL" and "line" not in each:
##                smellslst.append("全文件")
