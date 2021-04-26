import requests
import pandas
import numpy
import threading
import json
import time
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64
import sys

# 解析四种类型的题目
def jiexi():
    nowtime = int(time.time() * 1000)
    url = wangzhi + "/c27/online_courseware/schedule/score_detail/single/" + str(sku_id) + "/0/?_date=" + str(
        nowtime) + "&term=latest"
    response = requests.get(url, headers=headers1)
    returnJson = response.json()

    # 列表
    lianjie_list = []
    video_list = []
    taolun_list = []
    work_list = []
    exam_list = []

    # 防止未定义变量
    true = 1
    false = 0
    null = 2

    infos = returnJson["data"]["leaf_level_infos"]
    for info in infos:
        infoId = info["id"]

        user_score = info["user_score"]
        evaluation_id = str(info["evaluation_id"])

        if user_score == 0:

            if evaluation_id == "7":
                print("图文单元")
                lianjie_list.append(infoId)

            elif evaluation_id == "6":
                print("视频单元")
                video_list.append(infoId)

            elif evaluation_id == "10":
                print("讨论单元")
                taolun_list.append(infoId)

            elif evaluation_id == "11":
                print("作业单元")
                work_list.append(infoId)

            elif evaluation_id == "12":
                print("考试单元")
                exam_list.append(infoId)
    print(video_list, lianjie_list, taolun_list, work_list, exam_list)
    return video_list, lianjie_list, taolun_list, work_list, exam_list


def pass_lianjie(lianjie_list):
    for lianjie in lianjie_list:
        url = wangzhi + "/mooc-api/v1/lms/learn/user_article_finish/"+str(lianjie)+"/?cid="+str(classroom_id)+"&sid="+str(sku_id)+"&term=latest&uv_id=" + str(school_id)
        LianjieRequest = requests.request("get",url,headers=headers1)
        print(LianjieRequest.text)

#视频通过
def pass_video(video_list):
    url = wangzhi + "/video-log/heartbeat/"
    for video in video_list:
        nowtime = int(time.time() * 1000)
        payload = {"heart_data": [
            {"i": 5, "et": "heartbeat", "p": "web", "n": "sjy-cdn.xuetangx.com", "lob": "cloud4", "cp": 1, "fp": 0,
             "tp": 229.5, "sp": 1, "ts": str(nowtime), "u": int(user_id), "uip": "", "c": int(course_id),
             "v": int(video),
             "skuid": int(sku_id), "classroomid": str(classroom_id), "cc": "164E33FDCE3563DB9C33DC5901307461",
             "d": 941.8,
             "pg": str(video) + "_usk7", "sq": 11, "t": "video"}]}
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers = headers2, data = payload)
        url_video = wangzhi + "/video-log/get_video_watch_progress/?cid=" + str(course_id) + "&user_id=" + str(
            user_id) + "&classroom_id=" + str(classroom_id) + "&video_type=video&vtype=rate&video_id=" + str(
            video) + "&snapshot=1&term=latest&uv_id=" + str(school_id)
        length = json.loads(requests.get(url_video, headers = headers1).text)
        length = int(length["data"][str(video)]["video_length"])
        commonData = {
            "ts": str(nowtime),
            "u": int(user_id),
            "c": int(course_id),
            "skuid": int(sku_id),
            "classroomid": str(classroom_id),
            "i": 5,
            "et": "heartbeat",
            "p": "web",
            "n": "sjy-cdn.xuetangx.com",
            "lob": "cloud4",
            "fp": 0,
            "tp": 229.5,
            "sp": 1,
            "uip": "",
            "cc": "164E33FDCE3563DB9C33DC5901307461",
            "t": "video",
        }
        for number in range(2, length+20, 20):
            nowtime = int(time.time() * 1000)
            bufferList = []
            for sq in range(11, 16):
                cp = number + (sq - 11) * 5
                bufferList.append({
                    **commonData,
                    "cp": cp,
                    "sq": sq,
                    "v": int(video),
                    "d": length,
                    "pg": str(video) + "_usk7"
                })
            payload = {"heart_data": bufferList}
            payload = json.dumps(payload)
            response = requests.request("POST", url, headers = headers2, data = payload)
            if json.loads(response.text) != {}:
                print("视频已看完")
                break
            else:
                print("视频通过1次")
                time.sleep(1)

def pass_taolun(taolun_list):
    url = "https://kmust.yuketang.cn/pro/lms/"
    pass

def pass_work(work_list):

    for work in work_list:
        url = wangzhi + "/mooc-api/v1/lms/learn/leaf_info/" + str(classroom_id) + "/" + str(work) + "/?sign=" + str(
            term_id) + "&term=latest&uv_id=" + str(school_id)
        res4 = json.loads(requests.get(url, headers = headers1).text)
        exercise_id = res4["data"]["content_info"]["leaf_type_id"]
        url = wangzhi + "/mooc-api/v1/lms/exercise/get_exercise_list/" + str(
            exercise_id) + "/?term=latest&uv_id=" + str(school_id)
        res3 = json.loads(requests.get(url, headers = headers1).text)

        # 匹配多选题答题
        for i in range(len(res3["data"]["problems"])):
            if str(res3["data"]["problems"][i]["user"]["is_show_answer"]) == str(False) and \
                    str(res3["data"]["problems"][i]["content"]["TypeText"]) == '单选题':
                print("单选题")
                problem_id = res3["data"]["problems"][i]["problem_id"]
                question = re.sub(r'<\/?((?!img).)*?\/?>', "", res3["data"]["problems"][i]["content"]["Body"])
                question = re.sub("\n+", "", question)
                question = question.lstrip()
                print(question)
                queryurl = "http://tiku.dandanla.cn/query"
                Queryform = {
                    "question":question[0:25]
                }
                try:
                    danxuan_answer = json.loads(requests.post(queryurl,data = Queryform).text)
                    answer = danxuan_answer["daan"]
                    print(answer)
                except:
                    continue

                # for kk in range(len(res3["data"]["problems"][i]["content"]["Options"])):
                    # if str(answer) in res3["data"]["problems"][i]["content"]["Options"][kk]["value"]:
                    #     requestsanswer = res3["data"]["problems"][i]["content"]["Options"][kk]["key"]
                url = wangzhi + "/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + str(school_id)
                if answer != "暂无答案":
                    payload = {"classroom_id": int(classroom_id), "problem_id": int(problem_id),
                               "answer": [str(answer)]}
                    pull_danxuan = requests.request("post", url, headers = headers3,
                                                    data = json.dumps(payload)).text
                    print("正确答案", answer)
                    print(pull_danxuan)
                else:
                    print("暂无答案")

                time.sleep(1)

        # 匹配多选题答题
            if str(res3["data"]["problems"][i]["user"]["is_show_answer"]) == str(False) and \
                    str(res3["data"]["problems"][i]["content"]["TypeText"]) == '多选题':
                print("多选题")
                problem_id = res3["data"]["problems"][i]["problem_id"]
                question = re.sub(r'<\/?((?!img).)*?\/?>', "", res3["data"]["problems"][i]["content"]["Body"])
                question = re.sub("\n+","",question)
                question = question.lstrip()
                print(question)
                queryurl = "http://tiku.dandanla.cn/query"
                Queryform = {
                    "question":question[0:25]
                }
                try:
                    duoxuan_answer = json.loads(requests.post(queryurl,data = Queryform).text)
                    duoxuan = duoxuan_answer["daan"].split(";")
                    print(duoxuan)
                except:
                    continue

                if duoxuan == ["暂无答案"]:
                    continue
                duo = []
                # for kk in range(len(res3["data"]["problems"][i]["content"]["Options"])):
                #     for aa in range(len(duoxuan)):
                #         if str(duoxuan[aa]) in res3["data"]["problems"][i]["content"]["Options"][kk]["value"]:
                #             requestsanswer = res3["data"]["problems"][i]["content"]["Options"][kk]["key"]
                #             duo.append(requestsanswer)
                #         else:
                #             requestsanswer = res3["data"]["problems"][i]["content"]["Options"][kk]["key"]
                #             print(requestsanswer, "选项未匹配")
                # if duo == []:
                #     continue
                # else:
                for kk in range(len(duoxuan)):
                    duo.append(duoxuan[kk])
                url = wangzhi + "/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + str(school_id)
                payload = {"classroom_id": int(classroom_id), "problem_id": int(problem_id),
                           "answer": duo}
                pull_danxuan = requests.request("post", url, headers = headers3,
                                                data = json.dumps(payload)).text
                print("正确答案", duo)
                print(pull_danxuan)

                time.sleep(1)

        # 匹配判断题答题
            if str(res3["data"]["problems"][i]["user"]["is_show_answer"]) == str(False) and \
                    str(res3["data"]["problems"][i]["content"]["TypeText"]) == '判断题':
                print("判断题")
                problem_id = res3["data"]["problems"][i]["problem_id"]
                question = re.sub(r'<\/?((?!img).)*?\/?>', "", res3["data"]["problems"][i]["content"]["Body"])
                question = re.sub("\n+","",question)
                question = question.lstrip()
                print(question)
                queryurl = "http://tiku.dandanla.cn/query"
                Queryform = {
                    "question":question[0:25]
                }
                try:
                    danxuan_answer = json.loads(requests.post(queryurl,data = Queryform).text)
                    answer = danxuan_answer["daan"]
                    if answer == "正确":
                        answer = "true"
                    if answer == "错误":
                        answer = "false"
                    print(answer)
                except:
                    continue

                requestsanswer = answer
                if requestsanswer == "暂无答案":
                    continue
                url = wangzhi + "/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + str(school_id)
                payload = {"classroom_id": int(classroom_id), "problem_id": int(problem_id),
                           "answer": [str(requestsanswer)]}
                pull_danxuan = requests.request("post", url, headers = headers3,
                                                data = json.dumps(payload)).text
                print("正确答案", requestsanswer)
                print(pull_danxuan)

                time.sleep(1)

            # 填空题作答
            if str(res3["data"]["problems"][i]["user"]["is_show_answer"]) == str(False) and \
                    str(res3["data"]["problems"][i]["content"]["TypeText"]) == '填空题':
                print("填空题")
                problem_id = res3["data"]["problems"][i]["problem_id"]
                question = re.sub(r'<\/?((?!img).)*?\/?>', "", res3["data"]["problems"][i]["content"]["Body"])
                question = re.sub("\n+", "", question)
                question = re.sub("\[填空1\]|\[填空2\]|\[填空3\]|\[填空4\]|\[填空5\]|"
                                  "\[填空6\]|\[填空7\]|\[填空8\]|\[填空9\]|\[填空10\]", "______ ", question)
                question = question.lstrip()
                print(question)
                queryurl = "http://tiku.dandanla.cn/query"
                Queryform = {
                    "question":question[0:25]
                }
                try:
                    duoxuan_answer = json.loads(requests.post(queryurl,data = Queryform).text)
                    duoxuan = duoxuan_answer["daan"].split("#")
                    print(duoxuan)
                except:
                    continue

                if duoxuan == ["暂无答案"]:
                    continue

                duo = {}
                for kk in range(len(duoxuan)):
                    duo[str(kk+1)] = duoxuan[kk]

                if duo == {}:
                    continue
                else:
                    url = wangzhi + "/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + str(school_id)
                    payload = {"classroom_id": int(classroom_id), "problem_id": int(problem_id),
                               "answers": duo}
                    print(payload)
                    pull_danxuan = requests.request("post", url, headers = headers3,
                                                    data = json.dumps(payload)).text
                    print("正确答案", duo)
                    print(pull_danxuan)

                time.sleep(1)

            time.sleep(1)
        print(work)

def pass_exam(exam_list):
    url = "https://kmust.yuketang.cn/pro/lms/"
    pass

def login(username,password):
    with open('ghost-public.pem') as f:
        key = f.read()
        pub_key = RSA.importKey(str(key))
        cipher = PKCS1_cipher.new(pub_key)
        rsa_text = base64.b64encode(cipher.encrypt(bytes(password.encode("utf8"))))
        password = rsa_text.decode('utf-8')

    payload = {"type": "PP", "name": username, "pwd": password}
    payload = json.dumps(payload)
    url = "https://www.yuketang.cn/pc/login/verify_pwd_login"
    headers = {
        "Content-Type": "application/json",
    }
    res = requests.request("POST", url, headers = headers, data = payload)
    if "false" in res.text:
        print("登陆失败")
        sys.exit(0)
    else:
        print("登陆成功")
    set_cookie = res.headers["Set-Cookie"]
    set_csrftoken = re.findall("csrf([\s\S]*)sessionid=", set_cookie)[0]
    set_csrftoken = re.findall("token=([\s\S]*); expires=", set_csrftoken)[0]
    set_sessionid = re.findall("sessionid=([\s\S]*); expires", set_cookie)[0]
    return_cookie = "csrftoken="+set_csrftoken+"; sessionid=" + set_sessionid
    print(return_cookie)

    return return_cookie,set_csrftoken

if __name__ == '__main__':

    # 传入参数
    global x_csrftoken
    global cookie
    global classroom_id

    # 登陆
    username = input("输入username")
    password = input("输入password")
    cookie, x_csrftoken = login(username,password)

    #课程id
    classroom_id = input("输入classroom_id")

    # 需要获取的参数
    global school_id
    global course_id
    global sku_id
    global user_id
    global wangzhi
    global term_id

    true = 1
    false = 2
    null = 3

    # cookie设置 跨域设置
    headers = {
        "Cookie": cookie,
        "x-csrftoken": x_csrftoken
    }

    # 获取学堂云4.0网址和course_id
    url = "https://www.yuketang.cn/v2/api/web/classrooms/" + str(classroom_id) + "?role=5"
    res = requests.request("GET",url,headers=headers)
    content = json.loads(res.text)
    course_id = content["data"]["course_id"]
    wangzhi = content["data"]["university_domain"]
    print(course_id)
    print(wangzhi)

    # 获取school_id
    nowtime = int(time.time()*1000)
    url = "https://www.yuketang.cn/edu_admin/get_university_info/?date_time=" + str(nowtime)
    res = json.loads(requests.get(url, headers = headers).text)
    school_id = res["data"]["bind_schools"][0]["id"]
    print(school_id)

    # 更新cookie
    url = wangzhi + "/edu_admin/get_user_basic_info/?term=latest&uv_id=" + str(school_id)
    cookie1 = requests.get(url,headers=headers).headers["Set-Cookie"]
    print(cookie1)
    new_csrftoken = re.findall("csrf([\s\S]*)sessionid=", cookie1)[0]
    new_csrftoken = re.findall("token=([\s\S]*); expires=", new_csrftoken)[0]
    new_sessionid = re.findall("sessionid=([\s\S]*); expires", cookie1)[0]
    new_cookie = "university_id="+str(school_id)+"; platform_id=3; csrftoken="+new_csrftoken+"; sessionid="+new_sessionid

    #更新headers.findall(
    headers1 = {
        "Cookie":new_cookie,
        "x-csrftoken":new_csrftoken,
        "xtbz":"cloud",
        "university-id":str(school_id)
    }
    print(headers1)

    headers2 = {
        "Cookie":new_cookie,
        "Content-Type": "application/json"
    }

    headers3 = {
        "Cookie":new_cookie,
        "x-csrftoken":new_csrftoken,
        "xtbz":"cloud",
        "university-id":str(school_id),
        "Content-Type": "application/json"
    }

    # 获取sku_id
    url = wangzhi + "/mooc-api/v1/lms/user/user-courses/?status=1&page=1&no_page=1&term=latest&uv_id=" + str(school_id)
    res1 = requests.request("GET",url,headers=headers1)
    content1 = json.loads(res1.text)
    for i in range(int(content1["data"]["count"])):
        if str(content1["data"]["product_list"][i]["classroom_id"]) == str(classroom_id):
            sku_id = content1["data"]["product_list"][i]["sku_id"]
            term_id = content1["data"]["product_list"][i]["course_sign"]
            break
    print(sku_id)

    # 获取user_id
    url = wangzhi + "/edu_admin/user/info?term=latest&uv_id=" + str(school_id)
    res = json.loads(requests.get(url, headers = headers1).text)
    user_id = res["data"]["sys_user_id"]
    print(user_id)

    # 获得解析类型
    video_list, lianjie_list, taolun_list, work_list, exam_list = jiexi()

    pass_lianjie(lianjie_list)
    pass_video(video_list)
    pass_taolun(taolun_list)
    pass_work(work_list)
    pass_exam(exam_list)