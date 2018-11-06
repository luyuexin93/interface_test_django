*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Test Cases ***
test_get_event_list
    ${payload}=     create dictionary       eid=1        # 创建字典类型对象eid 用于传参
    Create session      event       http://127.0.0.1:8000/api    # 创建http会话服务器 event 指定基础url
    ${r}=       Get Request     event       /get_event_list/    params=${payload}   # Get Request 发起get请求 接口url关键字拼接成
    should be equal as strings      ${r.status_code}        200          # 断言返回的状态码
    log     ${r.json()}
    ${dict}   set variable      ${r.json()}
    #断言结果
    ${msg}      Get From Dictionary     ${dict}     message
    should be equal     ${msg}    success

test_user_sign_success
    create session      sign        http://127.0.0.1:8000/api
    ${headers}      create dictionary       Content-Type=application/x-www-form-urlencoded
    ${payload}      create dictionary        eid=11      phone=13122002200
    ${r}=       post request    sign    /user_sign/     data=${payload}     headers=${headers}
    should be equal as strings      ${r.status_code}    200
    log  ${r.json()}
    ${dict}     set variable        ${r.json()}
    # 断言结果
    ${msg}      get from dictionary     ${dict}     message
    should be equal     ${msg}      sign success
    ${sta}      Get from dictionary     ${dict}     status
    ${status}       evaluate    int(200)
    should be equal     ${sta}      ${status}

