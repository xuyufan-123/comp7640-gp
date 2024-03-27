# import caching as caching
from flask import Flask, jsonify, request
from sqlalchemy import text
import auth
from config import BaseConfig
from flask_sqlalchemy import  SQLAlchemy
# from aliyunsms.sms_send import send_sms
import json
import random
import datetime
from redis import StrictRedis

# 创建redis对象
redis_store = StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())



# login
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():
    print(request.json)
    userortel = request.json.get("userortel").strip()
    password = request.json.get("password").strip()
    role = request.json.get("role").strip()
    print(userortel)
    print(password)
    print(role)
    if role == "0":

        sql = ('select * ' \
               + 'from customer ' \
               + 'where cust_phone = "{0}" and password = "{1}"').format(userortel, password)
        data = db.session.execute(text(sql)).first()
        print(data)
        if data != None:
            customer = {'id': data[0], 'username': data[1], 'password': data[2], 'telephone': data[3], 'address':data[4]}
            # 生成token
            token = auth.encode_func(customer)
            print(token)
            customer_id = data[0]
            return jsonify(status=200, msg="登录成功", token=token, customer_id=customer_id)
        else:
            return jsonify(status=1000, msg="用户名或密码错误")

    if role == "1":

        sql = ('select * ' \
               + 'from vendor ' \
               + 'where vd_phone = "{0}" and password = "{1}"').format(userortel, password)
        data = db.session.execute(text(sql)).first()
        print(data)
        if data != None:
            vendor = {'id': data[1], 'username': data[2], 'password': data[5]}
            # 生成token
            token = auth.encode_func(vendor)
            print(token)
            vendor_id = data[1]
            return jsonify(status=200, msg= "登录成功", token=token, vendor_id=vendor_id)
        else:
            return jsonify(status=1000, msg="用户名或密码错误")
    else:
        return jsonify(status=1000, msg="请选择身份")

# sign up
@app.route("/api/user/register/test", methods=["POST"])
@cross_origin()
def register_test():
    rq = request.json
    username = rq.get("username")
    password = rq.get("password")
    telephone = rq.get("telephone")
    role = rq.get("role")

    if role == "0":

        lastest_customer_id = db.session.execute(text('select id from customer')).fetchall()
        print(lastest_customer_id[-1][0])
        customer_id = lastest_customer_id[-1][0]+1

        data = db.session.execute(text('select * from customer where cust_phone="%s"' % telephone)).fetchall()

        if not data:
            db.session.execute(text('insert into customer(id,name,password,cust_phone,address) value("%d","%s","%s","%s", "%s")' % (
                customer_id, username, password, telephone, '')))

            db.session.commit()
            return jsonify(status=200, msg="注册成功")
        else:
            return jsonify(status=1000, msg="该用户已存在")

    if role == "1":
        lastest_vendor_id = db.session.execute(text('select vendor_id from vendor')).fetchall()
        print(lastest_vendor_id[-1][0])
        vendor_id = lastest_vendor_id[-1][0] + 1
        score = 0

        data = db.session.execute(text('select * from vendor where vd_phone="%s"' % telephone)).fetchall()

        if not data:
            db.session.execute(text('insert into vendor(vendor_id,vendor_name,score_ave,vd_phone,password) value("%d","%s","%s","%s","%s")' % (
                vendor_id, username, score, telephone, password)))
            db.session.commit()
            return jsonify(status=200, msg="注册成功")
        else:
            return jsonify(status=1000, msg="该用户已存在")

# customer view vendor list
@app.route("/api/user/vendor", methods=["GET"])
@cross_origin()
def user_get_vendor():
    data = db.session.execute(text('select * from vendor')).fetchall()
    print(data)
    Data = []
    for i in range(len(data)):
        dic = dict(vendor_id=data[i][1], vendor_name=data[i][2], score=data[i][3])
        Data.append(dic)
    # return jsonify({"status":"200", "tabledata": Data})
    return jsonify(status=200, vendor=Data)

# customer view product list
@app.route("/api/user/product", methods=["POST"])
@cross_origin()
def user_get_product():
    print(request.json)
    rq = request.json
    vendor_id = rq.get("vendor_id")
    print(vendor_id)
    data = db.session.execute(text(('SELECT product_id, product_name, price_pd, inventory, colour, thickness, size FROM product, tag WHERE tag.p_id= product.product_id AND vendor_id = {0}').format(vendor_id))).fetchall()
    print(data)
    Data = []
    for i in range(len(data)):
        dic = dict(product_id=data[i][0], product_name=data[i][1], price=data[i][2], inventory=data[i][3], colour=data[i][4], thickness=data[i][5], size=data[i][6])
        Data.append(dic)
    print(Data)
    return jsonify(status=200, product=Data)


# place orders
@app.route("/api/user/addorder", methods=["POST"])
@cross_origin()
def user_addorder():
    rq = request.json
    orderlist = rq.get("orderlist")
    customer_id = rq.get("customer_id")
    lastest_order = db.session.execute(text('SELECT `order` FROM `order`')).fetchall()
    order = lastest_order[-1][0] + 1
    for i in range(len(orderlist)):
        product_id = orderlist[i].get("product_id")
        vendor_id = orderlist[i].get("vendor_id")
        purchase_count = orderlist[i].get("purchase_count")
        print(product_id)

        inventory = db.session.execute(text(('SELECT inventory FROM `product` WHERE product_id= {0}').format(product_id))).fetchall()
        print("inventory", inventory)
        Inventory = inventory[0][0]
        print(Inventory)

        if(Inventory!=0):
            db.session.execute(text(('UPDATE product SET inventory = "{0}" WHERE product_id = {1}').format(Inventory-purchase_count, product_id)))
            db.session.commit()

            lastest_order_id = db.session.execute(text('SELECT order_id FROM `order` ORDER BY order_id')).fetchall()
            order_id = lastest_order_id[-1][0] + 1


            status = "Order confirmed"
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.execute(text('insert into `order`'
                                     +'(order_id, vendor_id, product_id, customer_id, `status`, date, `order`, purchase_count)'
                                      + 'value("%d", "%d", "%d", "%d","%s","%s","%d","%d")' % (
                order_id, vendor_id, product_id, customer_id, status, date, order, purchase_count)))
            db.session.commit()

        else:
            return jsonify(status=1000, msg="Insufficient stock of the product")
    return jsonify(status=200, msg="Order confirmed")


# view order
@app.route("/api/user/vieworder", methods=["POST"])
@cross_origin()
def user_vieworder():
    rq = request.json
    customer_id=rq.get("customer_id")

    order = db.session.execute(text(('SELECT order_id, `order`, purchase_count, product_name, vendor_name, price_pd, status, date FROM `order`,`vendor`,`product` WHERE order.customer_id="{0}" and order.product_id=product.product_id and order.vendor_id=vendor.vendor_id').format(customer_id))).fetchall()
    print(order)
    if(order != []):
        total_order = []
        for i in range(len(order)):
            dic = dict(order_id=order[i][0], ordernum=order[i][1], purchase_count=order[i][2], product_name=order[i][3], vendor_name=order[i][4], price_pd=order[i][5], status=order[i][6], date=order[i][7] )
            total_order.append(dic)
        return jsonify(status=200, msg="viewing total_order", total_order=total_order)
    else:
        return jsonify(status=1000, msg="empty order")

@app.route("/api/user/deleteorder", methods=["POST"])
@cross_origin()
def user_deleteorder():

    rq = request.json
    order_id=rq.get("order_id")
    status = db.session.execute(text(('SELECT status FROM `order` WHERE order_id="{0}" ').format(order_id))).fetchall()
    if(status[0][0]=="Order confirmed"):
        db.session.execute(
            text(('DELETE FROM `order` WHERE order_id = {0}').format(order_id)))
        db.session.commit()
        return jsonify(status=200, msg="delete succeeded")
    else:
        return jsonify(status=1000, msg="This products is Non-returnable ")


@app.route("/api/user/score", methods=["POST"])
@cross_origin()
def user_score():
    rq = request.json
    score = rq.get("score")
    vendor_id = rq.get("vendor_id")
    score_info = db.session.execute(text(('SELECT score_ave, score_count FROM vendor WHERE vendor_id={0}').format(vendor_id))).fetchall()
    print(score_info)
    score_count = score_info[0][1]+1
    score_ave = (score_info[0][0]*score_info[0][1] + score)/score_count
    print(score_count, score_ave)
    db.session.execute(text(
        ('UPDATE vendor SET score_ave = {0}, score_count= {1} WHERE vendor_id = {2}').format(score_ave, score_count, vendor_id)))
    db.session.commit()
    return jsonify(status=200, msg="score succeeded")

@app.route("/api/user/showtags", methods=["GET"])
@cross_origin()
def user_showtags():

    data_colour = db.session.execute(text('SELECT DISTINCT colour FROM tag')).fetchall()
    colour = []
    print(data_colour[1][0])
    for i in range(len(data_colour)):
        colour.append(data_colour[i][0])

    data_thickness = db.session.execute(text('SELECT DISTINCT thickness FROM tag')).fetchall()
    thickness = []
    for i in range(len(data_thickness)):
        thickness.append(data_thickness[i][0])

    data_size = db.session.execute(text('SELECT DISTINCT size FROM tag')).fetchall()
    size = []
    for i in range(len(data_size)):
        size.append(data_size[i][0])
    return jsonify(status=200, colour=colour, thickness=thickness, size=size)

@app.route("/api/user/searchwithtags", methods=["POST"])
@cross_origin()
def user_searchwithtags():
    rq = request.json
    vendor_id = rq.get("vendor_id")
    colour = rq.get("colour")
    thickness = rq.get("thickness")
    size = rq.get("size")
    Data = db.session.execute(text(('SELECT product.product_id, product.product_name, product.price_pd, product.inventory FROM product JOIN tag ON tag.p_id = product.product_id WHERE tag.colour ="{0}" AND tag.thickness = "{1}" AND tag.size = "{2}" AND vendor_id={3}').format(colour, thickness, size, vendor_id))).fetchall()
    if(Data!=None):
        data = []
        for i in range(len(Data)):
            dic = dict(product_id=Data[i][0], product_name=Data[i][1], price=Data[i][2], inventory=Data[i][3],colour=colour, thickness=thickness, size=size)
            data.append(dic)
        return jsonify(status=200, product=data)
    else:
        return jsonify(status=200, msg="No result")
##################################################################################################################################################################################



# vendor viewing product
@app.route("/api/vendor/getproduct", methods=["POST"])
@cross_origin()
def vendor_get_product():
    print(request.json)
    rq = request.json
    vendor_id = rq.get("vendor_id")
    print(vendor_id)
    data = db.session.execute(text(('SELECT product_id, product_name, price_pd, inventory, colour, thickness, size FROM product, tag WHERE tag.p_id=product.product_id AND vendor_id = {0}').format(vendor_id))).fetchall()
    Data = []
    for i in range(len(data)):
        dic = dict(product_id=data[i][0], product_name=data[i][1], price=data[i][2], inventory=data[i][3],colour=data[i][4],thickness=data[i][5],size=data[i][6])
        Data.append(dic)
    print(Data)
    return jsonify(status=200, product=Data)

# vendor add product
@app.route("/api/vendor/addproduct", methods=["POST"])
@cross_origin()
def vendor_add_product():
    print(request.json)
    rq = request.json
    product_name = rq.get("product_name")
    vendor_id = rq.get("vendor_id")
    price_pd = rq.get("price_pd")
    inventory = rq.get("inventory")
    colour=rq.get("colour")
    thickness=rq.get("thickness")
    size=rq.get("size")

    lastest_product_id = db.session.execute(text('SELECT product_id FROM `product`')).fetchall()
    product_id = lastest_product_id[-1][0] + 1
    print(product_id)
    lastest_tag_id = db.session.execute(text('SELECT tagid FROM `tag`')).fetchall()
    tag_id = lastest_tag_id[-1][0] + 1
    print(tag_id)
    db.session.execute(text('insert into `product`'
                            + '(product_id, product_name, vendor_id, price_pd, inventory)'
                            + 'value("%d", "%s", "%d", "%d","%d")' % (
                                product_id, product_name, vendor_id, price_pd, inventory)))
    db.session.commit()
    db.session.execute(text('insert into `tag`'
                            + '(tagid, p_id, colour, thickness, size)'
                            + 'value("%d", "%d", "%s", "%s","%s")' % (
                                tag_id, product_id, colour, thickness, size)))
    db.session.commit()
    return jsonify(status=200, msg="add product succeeded")

# vendor modify product
@app.route("/api/vendor/modifyproduct", methods=["POST"])
@cross_origin()
def vendor_modify_product():
    print(request.json)
    rq = request.json
    product_id = rq.get("product_id")
    product_name = rq.get("new_product_name")
    price_pd = rq.get("new_price_pd")
    inventory = rq.get("new_inventory")
    db.session.execute(
        text(('UPDATE product SET product_name="{0}", price_pd ={1}, inventory = {2} WHERE product_id = {3}').format(product_name, price_pd, inventory, product_id)))
    db.session.commit()
    return jsonify(status=200, msg="update product succeeded")

# vendor delete product
@app.route("/api/vendor/deleteproduct", methods=["POST"])
@cross_origin()
def vendor_delete_product():
    print(request.json)
    rq = request.json
    product_id = rq.get("product_id")
    db.session.execute(
        text(('DELETE FROM product WHERE product_id = {0}').format(product_id)))
    db.session.commit()
    return jsonify(status=200, msg="delete product succeeded")

# vendor view order
@app.route("/api/vendor/vieworder", methods=["POST"])
@cross_origin()
def vendor_vieworder():
    rq = request.json
    vendor_id=rq.get("vendor_id")
    # 获取各个参数
    order = db.session.execute(text(('SELECT `order_id`, customer_id, product_name, price_pd, `status`, date, address FROM customer, `order`,`vendor`,`product` WHERE customer.id=`order`.customer_id AND `order`.product_id=product.product_id and `order`.vendor_id={0}').format(vendor_id))).fetchall()
    print(order)
    if(order != []):
        total_order = []
        for i in range(len(order)):
            dic = dict(orderid=order[i][0], customer_id=order[i][1], product_name=order[i][2], price_pd=order[i][3], status=order[i][4], date=order[i][5], address=order[i][6])
            total_order.append(dic)
        return jsonify(status=200, msg="viewing order", total_order=total_order)
    else:
        return jsonify(status=1000, msg="empty order")

# vendor modify order status
@app.route("/api/vendor/updatestatus", methods=["POST"])
@cross_origin()
def vendor_update_status():
    print(request.json)
    rq = request.json
    order_id = rq.get("order_id")
    status = rq.get("new_status")
    db.session.execute(
        text(('UPDATE `order` SET status = "{0}" WHERE order_id = {1}').format(status, order_id)))
    db.session.commit()
    return jsonify(status=200, msg="update status succeeded")



# def get_token_phone(token):
#     data = auth.decode_func(token)
#     phone = data['telephone']
#     return (phone)
#
#
# @app.route("/api/user/unsend", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# #删除订单
# #修改订单
# def user_unsend():
#     if request.method == 'GET':
#         phone = get_token_phone(request.headers.get('token'))
#         print(phone)
#         data = db.session.execute(text('select * from oorder where checked=0 and cons_phone="%s"' % phone)).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2], orderway=data[i][3],
#                        cons_name=data[i][5], cons_addre=data[i][6], create_time=data[i][8])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#     if request.method == 'POST':
#         rq = request.json
#         order_id = rq.get("order_id")
#         cons_name = rq.get("cons_name")
#         cons_addre = rq.get("cons_addre")
#         print(order_id)
#         db.session.execute(
#             text('update oorder set cons_name="%s", cons_addre="%s" where order_id="%d"' % (cons_name, cons_addre, order_id)))
#         db.session.commit()
#         return jsonify(status=200, msg="修改成功")
#     if request.method == 'DELETE':
#         order_id = request.json.get("delete_id")
#         db.session.execute(text('delete from oorder where order_id="%d" ' % order_id))
#         db.session.commit()
#         return jsonify(status=200, msg="删除成功")
#
#
# @app.route("/api/user/sending", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# def user_sending():
#     if request.method == 'GET':
#         phone = get_token_phone(request.headers.get('token'))
#
#         data = db.session.execute(text('select * from sending_order where cons_phone="%s"' % phone)).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
#                        cons_phone=data[i][4],
#                        cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8],
#                        disp_phone=data[i][9])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#
#
# @app.route("/api/user/sended", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# def user_sended():
#     if request.method == 'GET':
#         phone = get_token_phone(request.headers.get('token'))
#         data = db.session.execute(text('select * from sended_order where cons_phone="%s"' % phone)).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
#                        cons_phone=data[i][4],
#                        cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8],
#                        disp_phone=data[i][9])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#
#
# @app.route("/api/user/usermsg", methods=["POST", "GET"])
# @cross_origin()
# def usermsg():
#     if request.method == 'GET':
#         phone = get_token_phone(request.headers.get('token'))
#         data = db.session.execute(text('select * from user_msg where phone="%s"' % phone)).fetchall()
#         Data = dict(real_name=data[0][1], sex=data[0][2], age=data[0][3], mail=data[0][4], phone=data[0][5],
#                    user_name=data[0][6])
#
#         return jsonify(status=200, data=Data)
#
#
# @app.route("/api/user/pwd_chg", methods=["POST"])
# @cross_origin()
# def user_pwd_chg():
#     if request.method=='POST':
#         pwd=request.json.get('new_pwd')
#         old_pwd=request.json.get('old_pwd')
#         phone = get_token_phone(request.headers.get('token'))
#         data = db.session.execute(text('select * from user where telephone="%s" and password="%s"'% (phone,old_pwd))).fetchall()
#         if not data:
#             return jsonify(status=1000,msg="原始密码错误")
#         else:
#             db.session.execute(text('update user set password="%s" where telephone="%s"'% (pwd,phone)))
#             db.session.commit()
#             return jsonify(status=200,msg="修改成功")
#
#
# @app.route("/api/manager/shop", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# def manager_shop():
#     # 获取店铺信息
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from fastfood_shop')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(shop_name=data[i][0], price=data[i][1], sale=data[i][2])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#     if request.method == 'POST' and request.json.get('action') == "add":
#         rq = request.json
#         shop_name = rq.get('shop_name')
#         price = rq.get('price')
#         m_sale_v = rq.get('m_sale_v')
#         exist = db.session.execute(text('select * from fastfood_shop where shop_name="%s"' % shop_name)).fetchall()
#         if not exist:
#             db.session.execute(text('insert fastfood_shop(shop_name,price,m_sale_v) value("%s",%d,%d)' % (
#                 shop_name, int(price), int(m_sale_v))))
#             db.session.commit()
#             return jsonify(status=200, msg="添加成功")
#         else:
#             return jsonify(status=1000, msg="该店铺已存在")
#
#     if request.method == 'POST' and request.json.get('action') == "change":
#         rq = request.json
#         shop_name = rq.get('shop_name')
#         price = rq.get('price')
#         m_sale_v = rq.get('m_sale_v')
#         db.session.execute(text('update fastfood_shop set price="%d", m_sale_v="%d" where shop_name="%s" ' % (
#             int(price), int(m_sale_v), shop_name)))
#         db.session.commit()
#         return jsonify(status=200, msg="修改成功")
#     if request.method == 'DELETE':
#         want_delete = request.json.get('want_delete')
#         db.session.execute(text('delete from fastfood_shop where shop_name="%s"' % want_delete))
#         db.session.commit()
#         return jsonify(status=200, msg="删除成功")
#
#
# @app.route("/api/manager/server", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# def manager_server():
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from server')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(service_id=data[i][0], service_name=data[i][1], fastfood_shop_name=data[i][2])
#             Data.append(dic)
#         shop_range = db.session.execute(text('select shop_name from fastfood_shop')).fetchall()
#         Shop = []
#         for i in range(len(shop_range)):
#             dic = dict(shop_name=shop_range[i][0])
#             Shop.append(dic)
#         print(Shop)
#         return jsonify(status=200, tabledata=Data, shop_range=Shop)
#     if request.method == 'POST':
#         rq = request.json
#         service_id = rq.get('service_id')
#         service_name = rq.get('service_name')
#         fastfood_shop_name = rq.get('fastfood_shop_name')
#         exist = db.session.execute(text('select * from server where service_id="%s"' % service_id)).fetchall()
#         if not exist:
#             db.session.execute(text('insert server(service_id,service_name,fastfood_shop_name) value("%s","%s","%s")' % (
#                 service_id, service_name, fastfood_shop_name)))
#             db.session.commit()
#             return jsonify(status=200, msg="添加成功")
#         else:
#             return jsonify(status=1000, msg="该编号已存在")
#     if request.method == 'DELETE':
#         want_delete = request.json.get('want_delete')
#         db.session.execute(text('delete from server where service_id="%s"' % want_delete))
#         db.session.commit()
#         return jsonify(status=200, msg="解雇成功")
#
#
# @app.route("/api/manager/dispatcher", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# def manager_dispatcher():
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from dispatcher')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(dispatcher_id=data[i][0], dispatcher_name=data[i][1], dispatcher_phone=data[i][2])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#     if request.method == 'POST':
#         rq = request.json
#         dispatcher_id = rq.get('dispatcher_id')
#         dispatcher_name = rq.get('dispatcher_name')
#         dispatcher_phone = rq.get('dispatcher_phone')
#         exist = db.session.execute(text('select * from dispatcher where dispatcher_id="%s"' % dispatcher_id)).fetchall()
#         if not exist:
#             db.session.execute(
#                 text('insert dispatcher(dispatcher_id,dispatcher_name,dispatcher_phone) value("%s","%s","%s")' % (
#                     dispatcher_id, dispatcher_name, dispatcher_phone)))
#             db.session.commit()
#             return jsonify(status=200, msg="添加成功")
#         else:
#             return jsonify(status=1000, msg="该编号已存在")
#     if request.method == 'DELETE':
#         want_delete = request.json.get('want_delete')
#         db.session.execute(text('delete from dispatcher where dispatcher_id="%s"' % want_delete))
#         db.session.commit()
#         return jsonify(status=200, msg="解雇成功")
#
#
# @app.route("/api/manager/wuliu", methods=["GET"])
# @cross_origin()
# def manager_wuliu():
#     ended = request.args.get('id')
#     if ended == '0':
#         data = db.session.execute(text('select * from wuliu where ended=0')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#     else:
#         data = db.session.execute(text('select * from wuliu where ended=1')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#
#
# @app.route("/api/manager/unsend", methods=["GET", "POST"])
# @cross_origin()
# def manager_unsend():
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from oorder where checked=0')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2], orderway=data[i][3],
#                        cons_phone=data[i][4],
#                        cons_name=data[i][5], cons_addre=data[i][6], create_time=data[i][8])
#             Data.append(dic)
#
#         disp_range = db.session.execute(text('select * from dispatcher')).fetchall()  # 获取所有的送货员就id，供选择
#         Disp_range = []
#         for i in range(len(disp_range)):
#             dic = dict(disp_id=disp_range[i][0])
#             Disp_range.append(dic)
#         return jsonify(status=200, tabledata=Data, disp_range=Disp_range)
#     if request.method == 'POST':
#         rq = request.json
#         order_id = rq.get('order_id')
#         disp_id = rq.get('dispatcher_id')
#         deliver_time = rq.get('deliver_time')
#         cons_phone = db.session.execute(text('select cons_phone from oorder where order_id="%d"' % int(order_id))).first()
#
#         db.session.execute(text('insert wuliu( order_id, cons_phone,disp_id,deliver_time) value(%d,"%s","%s","%s")' % (
#         int(order_id), cons_phone[0], disp_id, deliver_time)))
#         db.session.commit()
#         return jsonify(status=200, msg="成功派发")
#
#
# @app.route("/api/manager/sending", methods=["GET"])
# @cross_origin()
# def manager_sending():
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from sending_order')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
#                        cons_phone=data[i][4],
#                        cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
#
#
# @app.route("/api/manager/sended", methods=["GET"])
# @cross_origin()
# def manager_sended():
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from sended_order')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
#                        cons_phone=data[i][4],
#                        cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8])
#             Data.append(dic)
#         return jsonify(status=200, tabledata=Data)
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
    # 开启了debug模式
