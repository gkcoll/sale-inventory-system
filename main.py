'''
@File    :   main.py
@Time    :   2023/04/26 23:33:43
@Author  :   @灰尘疾客
@Version :   1.0
@Site    :   https://www.gkcoll.xyz
@Desc    :   A simple self service sales and inventory system.
@Refer to:   https://github.com/iiamjune/simple-sales-and-inventory
'''


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os.path
import os
from datetime import datetime


signed = False
window = Tk()
window.title("售货与库存")

# Set a icon for window
# See https://www.gkcoll.xyz/486.html
try:
    window.iconbitmap('logo.ico')
except:
    from fav import icon
    from base64 import b64decode as a

    with open('logo.ico', 'wb') as f:
        f.write(a(icon))
    window.iconbitmap('logo.ico')

sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
ww = 800
wh = 600
x = (sw-ww) / 2
y = (sh-wh) / 2
window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
window.resizable(False, False)
style = ttk.Style()
style.theme_use("clam")

addinput_itemname = StringVar()
addinput_price = StringVar()
addinput_quantity = StringVar()
editinput_itemname = StringVar()
editinput_price = StringVar()
editinput_quantity = StringVar()
editinput_search = StringVar()
purchaseinput_search = StringVar()
purchaseinput_itemname = StringVar()
purchaseinput_quantity = StringVar()
purchase_carttotal = StringVar()
purchase_total = 0.0
purchase_subtotal = 0.0
purchase_checkoutitemname = StringVar()
purchase_checkoutquantity = StringVar()
purchase_checkoutinvoice = StringVar()
purchase_checkoutdatetime = StringVar()


def only_numbersdecimal(char: str):
    return char.isdigit() or char == '.'


def only_numbers(char: str):
    return char.isdigit()


def _len(s):
    return sum([2 if '\u4e00' <= i <= '\u9fff' else 1 for i in s])


def white(quantity: int):
    return ' ' * quantity


price_validation = window.register(only_numbersdecimal)
quantity_validation = window.register(only_numbers)


def add_back():
    main_window()
    addinput_itemname.set('')
    addinput_price.set('')
    addinput_quantity.set('')


def add_items():
    itemname_iscorrect = False
    price_iscorrect = False
    quantity_iscorrect = False
    items_dict = {}

    if not addinput_itemname.get() or len(addinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('错误', '请输入项目名')
    else:
        if ' ' in addinput_itemname.get():
            messagebox.showerror('警告', '项目名不能包含空格。\n使用 "-" 以连接大于一个单词的项目名。')
        else:
            itemname_iscorrect = True
            item_name = addinput_itemname.get().strip().title()

    if not addinput_price.get() or addinput_price.get() == '.':
        price_iscorrect = False
        messagebox.showerror('错误', '请输入项目价格')
    else:
        price_iscorrect = True
        item_price = float(addinput_price.get())

    if not addinput_quantity.get() or int(addinput_quantity.get()) == 0:
        quantity_iscorrect = False
        messagebox.showerror('错误', '请输入项目库存')
    else:
        quantity_iscorrect = True
        item_quantity = int(addinput_quantity.get())

    if itemname_iscorrect and price_iscorrect and quantity_iscorrect:
        invItems = getInvItems()
        if item_name in invItems.keys():
            messagebox.showerror('错误', '项目已存在')
        else:
            items_dict[item_name] = [
                {"quantity": item_quantity}, {"price": item_price}]
            addinput_itemname.set('')
            addinput_price.set('')
            addinput_quantity.set('')
            add_items_to_file(items_dict, clear=False, message='项目添加成功')
            add_window()


def add_items_to_file(items_dict: dict, clear: bool, message: str):
    if clear:
        with open('inventory.txt', 'a', encoding='utf-8') as file:
            for item in items_dict:
                file.write(f'{item}: {items_dict[item]}')
                file.write('\n')
            messagebox.showinfo('成功', message)
        return
    invItems = getInvItems()

    for item in invItems:
        if item in items_dict:
            items_dict[item] += invItems[item]
    with open('inventory.txt', 'a', encoding='utf-8') as file:
        for item in items_dict:
            file.write(f'{item}: {items_dict[item]}')
            file.write('\n')
        messagebox.showinfo('成功', message)


def getInvItems():
    invItems = {}

    if os.path.exists('inventory.txt') == False:
        f = open('inventory.txt', 'w')
        f.close()
    else:
        with open('inventory.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '').split(' ')
                item_name, item_quantity, item_price = line[0].replace(
                    ':', ''), line[2].replace('},', ''), line[4].replace('}]', '')
                invItems.update(
                    {item_name: [{'quantity': int(item_quantity)}, {'price': float(item_price)}]})

    return invItems


def add_window():
    if signed:
        add_frame = Frame(window, width=800, height=600)
        add_frame.tk_setPalette(background='#E9EEF3', foreground='#2C4C71')
        add_frame.grid(row=0, column=0, sticky=NW)
        add_frame.propagate(0)
        add_frame.update()

        Label(
            add_frame,
            text='添加项目',
            font='Arial 18 bold').place(
                relx=.5,
                y=40,
                anchor=CENTER)
        Button(
            add_frame,
            text='返回',
            command=add_back,
            height=2,
            width=5,
            background='#2C4C71',
            foreground='#E9EEF3').place(
                relx=.04,
                y=40,
                anchor=CENTER)
        Label(
            add_frame,
            text='项目名',
            font='Arial 14 bold').place(
                x=60,
                y=160)
        Entry(
            add_frame,
            width=30,
            textvariable=addinput_itemname,
            font='Arial 14',
            foreground='black',
            highlightthickness=1,
            highlightbackground='#2C4C71',
            highlightcolor='#2C4C71').place(
                x=60,
                y=200)
        Label(
            add_frame,
            text='价格',
            font='Arial 14 bold').place(
                x=450,
                y=160)
        Entry(
            add_frame,
            width=25,
            textvariable=addinput_price,
            font='Arial 14',
            foreground='black',
            highlightthickness=1,
            highlightbackground='#2C4C71',
            highlightcolor='#2C4C71',
            validate='key',
            validatecommand=(price_validation, '%S')).place(
                x=450,
                y=200)
        Label(
            add_frame,
            text='库存',
            font='Arial 14 bold').place(
                x=450,
                y=250)
        Entry(
            add_frame,
            width=10,
            textvariable=addinput_quantity,
            font='Arial 14',
            foreground='black',
            highlightthickness=1,
            highlightbackground='#2C4C71',
            highlightcolor='#2C4C71',
            validate='key',
            validatecommand=(quantity_validation, '%S')).place(
                x=450,
                y=290)
        Button(
            add_frame,
            text='上架',
            command=add_items,
            height=8,
            width=30,
            background='#2C4C71',
            foreground='#E9EEF3').place(
                relx=.5,
                y=490,
                anchor=CENTER)
    else:
        messagebox.showwarning("非法操作", "此功能为管理员专用，您尚未登陆管理员账号，请先登录管理员账号！！！")


def view_back():
    main_window()
    editinput_itemname.set('')
    editinput_price.set('')
    editinput_quantity.set('')
    editinput_search.set('')


def view_binditem(e):
    value_list = []
    selected_item = view_treeview.focus()
    if selected_item:
        for value in view_treeview.item(selected_item)['values']:
            value_list.append(value)
        editinput_itemname.set('')
        editinput_itemname.set(str(value_list[0]))
        editinput_quantity.set('')
        editinput_quantity.set(str(value_list[1]))
        editinput_price.set('')
        editinput_price.set(str(value_list[2]))


def delete_item():
    itemname_iscorrect = False

    if not editinput_itemname.get() or len(editinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('错误', '请选择一个项目')
    else:
        itemname_iscorrect = True
        item_name = editinput_itemname.get().strip().title()

    if itemname_iscorrect:
        invItems = getInvItems()
        item_to_delete = item_name
        if item_to_delete in invItems.keys():
            confirm_delete = messagebox.askyesno(
                '删除项目', f'你确定要从仓库中删除 {item_name} 吗？')
            if confirm_delete:
                del invItems[item_to_delete]
                editinput_itemname.set('')
                editinput_price.set('')
                editinput_quantity.set('')
                editinput_search.set('')
                add_items_to_file(invItems, clear=True,
                                  message=f'{item_name} 已被成功删除')
                view_window()
        else:
            messagebox.showerror('错误', '项目不存在！')


def update_item():
    itemname_iscorrect = False
    price_iscorrect = False
    quantity_iscorrect = False

    if not editinput_itemname.get() or len(editinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('错误', '请选择一个项目')
    else:
        if ' ' in editinput_itemname.get():
            messagebox.showerror('警告', '项目名不能包含空格。\n使用 "-" 以连接单词数大于一的项目名。')
        else:
            itemname_iscorrect = True
            item_name = editinput_itemname.get().strip().title()

            if not editinput_price.get() or editinput_price.get() == '.' or float(editinput_price.get()) == 0:
                price_iscorrect = False
                messagebox.showerror('错误', '请输入项目价格')
            else:
                price_iscorrect = True
                item_price = float(editinput_price.get())

            if not editinput_quantity.get() or int(editinput_quantity.get()) == 0:
                quantity_iscorrect = False
                messagebox.showerror('错误', '请输入项目库存')
            else:
                quantity_iscorrect = True
                item_quantity = int(editinput_quantity.get())

    if itemname_iscorrect and price_iscorrect and quantity_iscorrect:
        invItems = getInvItems()
        item_to_change = item_name
        if item_to_change in invItems.keys():
            invItems.update(
                {item_name: [{'quantity': int(item_quantity)}, {'price': float(item_price)}]})

            editinput_itemname.set('')
            editinput_price.set('')
            editinput_quantity.set('')
            editinput_search.set('')
            add_items_to_file(invItems, clear=True, message='项目信息更新成功')
            view_window()
        else:
            messagebox.showerror('错误', '项目不存在！')


def view_searchitem():
    query = edit_searchentry.get().strip().title()
    selection = []
    for child in view_treeview.get_children():
        if query in view_treeview.item(child)['values']:
            selection.append(child)
            editinput_itemname.set(view_treeview.item(child)['values'][0])
            editinput_quantity.set(view_treeview.item(child)['values'][1])
            editinput_price.set(view_treeview.item(child)['values'][2])
    if len(selection) == 0:
        editinput_itemname.set('')
        editinput_quantity.set('')
        editinput_price.set('')
        messagebox.showinfo('信息', '没有找到相关结果')
    view_treeview.selection_set(selection)


def view_window():
    if signed:
        global view_treeview
        global edit_searchentry

        view_frame = Frame(window, width=800, height=600)
        view_frame.tk_setPalette(background='#E9EEF3', foreground='#2C4C71')
        view_frame.grid(row=0, column=0, sticky=NW)
        view_frame.propagate(0)
        view_frame.update()

        Label(
            view_frame,
            text='浏览项目',
            font='Arial 18 bold').place(
                relx=.5,
                y=40,
                anchor=CENTER)
        Button(
            view_frame,
            text='返回',
            command=view_back,
            height=2,
            width=5,
            background='#2C4C71',
            foreground='#E9EEF3').place(
                relx=.04,
                y=40,
                anchor=CENTER)
        edit_searchentry = Entry(
            view_frame,
            width=20,
            textvariable=editinput_search,
            font='Arial 8',
            foreground='black',
            highlightthickness=1,
            highlightbackground='#2C4C71',
            highlightcolor='#2C4C71')
        edit_searchbutton = Button(
            view_frame,
            text='搜索',
            command=view_searchitem,
            height=1,
            width=5,
            background='#2C4C71',
            foreground='#E9EEF3')
        edit_itemnamelabel = Label(
            view_frame,
            text='项目名',
            font='Arial 8')
        edit_itemnameentry = Entry(
            view_frame,
            width=30,
            textvariable=editinput_itemname,
            font='Arial 8',
            state=DISABLED)
        edit_quantitylabel = Label(
            view_frame,
            text='库存',
            font='Arial 8')
        edit_quantityentry = Entry(
            view_frame,
            width=10,
            textvariable=editinput_quantity,
            font='Arial 8')
        edit_pricelabel = Label(
            view_frame,
            text='价格',
            font='Arial 8')
        edit_priceentry = Entry(
            view_frame,
            width=25,
            textvariable=editinput_price,
            font='Arial 8')
        edit_updatebutton = Button(
            view_frame,
            text='更新',
            command=update_item,
            height=8,
            width=30,
            background='#2C4C71',
            foreground='#E9EEF3')
        edit_deletebutton = Button(
            view_frame,
            text='删除',
            command=delete_item,
            height=8,
            width=30,
            background='#2C4C71',
            foreground='#E9EEF3')

        cols = ('项目名', '库存', '价格')
        view_treeview = ttk.Treeview(view_frame, columns=cols, show='headings')

        invItems = getInvItems()
        if len(invItems) == 0:
            view_treeview.unbind('<ButtonRelease-1>')
            edit_searchentry.config(state='disabled')
            edit_searchbutton.config(state='disabled')
            edit_quantityentry.config(state='disabled')
            edit_priceentry.config(state='disabled')
            edit_updatebutton.config(state='disabled')
            edit_deletebutton.config(state='disabled')
            messagebox.showinfo('信息', '仓库里没有项目')
        else:
            view_treeview.bind('<ButtonRelease-1>', view_binditem)

        for col in cols:
            view_treeview.heading(col, text=col)
            view_treeview.grid(row=1, column=0, columnspan=2)
            view_treeview.column(col, anchor='center')
            view_treeview.place(relx=.5, rely=.4, anchor=CENTER)

        tempInvList = []
        for key, value in getInvItems().items():
            tempInvList.append([key, value[0]['quantity'], value[1]['price']])
        tempInvList.sort(key=lambda x: x[2])
        for i in enumerate(tempInvList, start=1):
            view_treeview.insert('', 'end', values=(i[1][0], i[1][1], i[1][2]))

        edit_searchentry.place(x=165, y=110, anchor=CENTER)
        edit_searchbutton.place(x=250, y=110, anchor=CENTER)

        edit_itemnamelabel.place(x=150, y=360)
        edit_itemnameentry.place(x=150, y=380)
        edit_quantitylabel.place(x=390, y=360)
        edit_quantityentry.place(x=390, y=380)
        edit_pricelabel.place(x=500, y=360)
        edit_priceentry.place(x=500, y=380)

        edit_updatebutton.place(relx=.3, y=500, anchor=CENTER)
        edit_deletebutton.place(relx=.7, y=500, anchor=CENTER)
    else:
        messagebox.showwarning("非法操作", "此功能为管理员专用，您尚未登陆管理员账号，请先登录管理员账号！！！")


def purchase_back():
    if len(purchase_carttreeview.get_children()) > 0:
        confirm_abort = messagebox.askyesno('中止操作', f'你确定要中止这个操作吗？')
        if confirm_abort:
            main_window()
            purchaseinput_itemname.set('')
            purchaseinput_quantity.set('')
            purchaseinput_search.set('')
    else:
        main_window()
        purchaseinput_itemname.set('')
        purchaseinput_quantity.set('')
        purchaseinput_search.set('')


def purchase_searchitem():
    query = purchase_searchentry.get().strip().title()
    selection = []
    for child in purchase_treeview.get_children():
        if query in purchase_treeview.item(child)['values']:
            selection.append(child)
            purchaseinput_itemname.set(
                purchase_treeview.item(child)['values'][0])
            purchaseinput_quantity.set('1')
    if len(selection) == 0:
        purchaseinput_itemname.set('')
        purchaseinput_quantity.set('')
        messagebox.showinfo('信息', '没有找到相关结果')
    purchase_treeview.selection_set(selection)


def purchase_binditem(e):
    value_list = []
    selected_item = purchase_treeview.focus()
    for value in purchase_treeview.item(selected_item)['values']:
        value_list.append(value)
    if len(value_list) > 0:
        purchaseinput_itemname.set('')
        purchaseinput_itemname.set(str(value_list[0]))
        purchaseinput_quantity.set('')
        purchaseinput_quantity.set('1')

        if purchaseinput_itemname.get() != '':
            purchase_addbutton.config(state=NORMAL)


def purchase_additem():
    itemname_iscorrect = False
    quantity_iscorrect = False

    if not purchaseinput_itemname.get() or len(purchaseinput_itemname.get().strip()) == 0:
        itemname_iscorrect = False
        messagebox.showerror('错误', '请选择一个项目')
    else:
        if ' ' in purchaseinput_itemname.get():
            messagebox.showerror('警告', '项目名不能包含空格。\n使用 "-" 以连接大于一个单词的项目名。')
        else:
            itemname_iscorrect = True
            item_name = purchaseinput_itemname.get().strip().title()

            if not purchaseinput_quantity.get() or int(purchaseinput_quantity.get()) == 0:
                quantity_iscorrect = False
                messagebox.showerror('错误', '请输入项目库存')
            else:
                quantity_iscorrect = True
                item_quantity = int(purchaseinput_quantity.get())

    if itemname_iscorrect and quantity_iscorrect:
        purchase_total = 0.0
        if getInvItems()[item_name][0]['quantity'] >= item_quantity:
            subtotal = getInvItems()[item_name][1]['price'] * item_quantity

            purchase_carttreeview.insert('', 'end', values=(
                item_name, item_quantity, subtotal))
            purchaseinput_itemname.set('')
            purchaseinput_quantity.set('')

            if len(purchase_carttreeview.get_children()) > 0:
                purchase_removebutton.config(state=NORMAL)
                purchase_checkoutbutton.config(state=NORMAL)

            for child in purchase_carttreeview.get_children():
                purchase_total += float(purchase_carttreeview.item(child)
                                        ['values'][2])
            purchase_carttotal.set(
                '总计: ￥' + str('{:.2f}'.format(purchase_total)))
        else:
            messagebox.showerror('错误', '库存不足')


def purchase_removeitem():
    current_row = purchase_carttreeview.focus()
    if not current_row:
        messagebox.showinfo('信息', '没有选择项目')
    else:
        selected_item = purchase_carttreeview.selection()[0]
        purchase_carttotal.set('总计: ￥' + str('{:.2f}'.format(float(purchase_carttotal.get(
        ).split('￥')[1]) - float(purchase_carttreeview.item(selected_item)['values'][2]))))
        purchase_carttreeview.delete(selected_item)

        if len(purchase_carttreeview.get_children()) == 0:
            purchase_removebutton.config(state=DISABLED)
            purchase_checkoutbutton.config(state=DISABLED)


def get_invoices():
    invoice_dict = {}

    if os.path.exists('invoice.txt') == False:
        f = open('invoice.txt', 'w', encoding='utf-8')
        f.close()
    else:
        with open('invoice.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '').split(' ')
                counter, invoice_id = line[0].replace(':', ''), line[1]
                invoice_dict.update({counter: invoice_id})

    return invoice_dict


def add_invoice(invoice_dict: dict, clear: bool):
    if clear:
        with open('invoice.txt', 'a', encoding='utf-8') as file:
            for invoice in invoice_dict:
                file.write(f"{invoice}: {invoice_dict[invoice]}")
                file.write('\n')
        return
    invoices = get_invoices()

    for invoice in invoices:
        if invoice in invoice_dict:
            invoice_dict[invoice] += invoices[invoice]
    with open('invoice.txt', 'a') as file:
        for invoice in invoice_dict:
            file.write(f"{invoice}: {invoice_dict[invoice]}")
            file.write('\n')


def generate_receipt(current_datetime: str, invoice_id: str, purchase_cartdata: dict, purchase_total: str):
    def g():
        maxname = max([max([_len(item) for item in purchase_cartdata]), 8])
        maxquantity = max([max([_len(str(i[0]['quantity']))
                                for i in purchase_cartdata.values()]), 4])
        maxprice = max([max([_len(str(i[0]['price']))
                       for i in purchase_cartdata.values()]), 4])
        maxsubtotal = max([max([_len(str(i[0]['subtotal']))
                                for i in purchase_cartdata.values()]), 4])

        current_info = "".join(
            ["交易时间: ", current_datetime, white(18), "发票号: ", invoice_id, "\n"])
        info_length = _len(current_info)

        table_width = max([maxname + maxquantity + maxprice +
                           maxsubtotal + 3, info_length])
        col_width = table_width // 4
        splitline = f"{'-'*table_width}\n"

        receipt_header = f"{'收据':^{table_width}}\n"

        receipt = splitline + receipt_header + splitline + current_info + splitline
        receipt += f"商品名称{white(col_width-8)} 数量{white(col_width-4)} 单价{white(col_width-4)} 小计{white(col_width-4)}\n"
        receipt += splitline

        for k, v in purchase_cartdata.items():
            name = k
            quantity = str(v[0]['quantity'])
            price = str(v[0]['price'])
            subtotal = str(v[0]['subtotal'])
            receipt += f"{name}{white(col_width-_len(name))} {quantity}{white(col_width-_len(quantity))} {price}{white(col_width-_len(price))} {subtotal}{white(col_width-_len(subtotal))}\n"

        receipt += f"{'-'*table_width}\n"
        receipt += f"{white(table_width-_len(purchase_total)-1)}{purchase_total}\n"
        receipt += f"{'-'*table_width}"

        return receipt
    receipt_list = []
    for file in os.listdir(os.getcwd()):
        if file.startswith('收据'):
            receipt_list.append(os.path.splitext(file)[0])

    if len(receipt_list) == 0:
        receipt_name = '收据-1'
        with open(f'{receipt_name}.txt', 'a', encoding='utf-8') as file:
            file.write(g())
    else:
        receipt_list.sort()
        receipt_list.reverse()
        receipt_name = f"收据-{int(receipt_list[0].split('-')[1]) + 1}"
        with open(f'{receipt_name}.txt', 'a', encoding='utf-8') as file:
            file.write(g())


def purchase_checkoutitems():
    global purchase_checkoutitemname
    global purchase_checkoutquantity
    global purchase_checkoutdatetime
    global purchase_checkoutinvoice
    global purchase_cartdata
    purchase_cartdata = {}
    invItems = getInvItems()

    for child in purchase_carttreeview.get_children():
        purchase_checkoutitemname.set(
            purchase_carttreeview.item(child)['values'][0])
        purchase_checkoutquantity.set(
            purchase_carttreeview.item(child)['values'][1])

        cart_itemname = purchase_carttreeview.item(child)['values'][0]
        cart_quantity = purchase_carttreeview.item(child)['values'][1]
        cart_price = invItems[cart_itemname][1]['price']
        cart_subtotal = purchase_carttreeview.item(child)['values'][2]
        purchase_cartdata.update({cart_itemname: [
                                 {'quantity': cart_quantity, 'price': cart_price, 'subtotal': cart_subtotal}]})

        item_to_change = purchase_checkoutitemname.get()
        if item_to_change in invItems.keys():
            item_quantity = invItems[item_to_change][0]['quantity'] - \
                int(purchase_checkoutquantity.get())
            item_price = invItems[item_to_change][1]['price']
            invItems.update({item_to_change: [{'quantity': int(
                item_quantity)}, {'price': float(item_price)}]})
        else:
            messagebox.showerror('错误', '项目不存在')

    current_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    purchase_checkoutdatetime.set(current_dt)

    invoices = get_invoices()
    counter_list = list(invoices.keys())
    if len(invoices) == 0:
        invoice_id = 'GK'+'1'.zfill(4)
        invoices.update({1: invoice_id})
        add_invoice(invoices, clear=False)
        purchase_checkoutinvoice.set(invoice_id)
    else:
        invoice_id = 'GK' + str(int(max(counter_list)) + 1).zfill(4)
        invoices[int(max(counter_list)) + 1] = invoice_id
        add_invoice(invoices, clear=True)
        purchase_checkoutinvoice.set(invoice_id)

    generate_receipt(purchase_checkoutdatetime.get(), purchase_checkoutinvoice.get(), purchase_cartdata, purchase_carttotal.get())
    add_items_to_file(invItems, clear=True, message='购物车结账成功')
    purchase_window()


def purchase_bindcartitem(e):
    value_list = []
    selected_item = purchase_carttreeview.focus()
    for value in purchase_carttreeview.item(selected_item)['values']:
        value_list.append(value)
    if len(value_list) > 0:
        global purchase_subtotal
        purchase_subtotal = 0.0
        purchase_subtotal += float(value_list[2])


def purchase_window():

    global purchase_treeview
    global purchase_searchentry
    global purchase_carttreeview
    global purchase_addbutton
    global purchase_removebutton
    global purchase_checkoutbutton

    purchase_frame = Frame(window, width=800, height=600)
    purchase_frame.tk_setPalette(background='#E9EEF3', foreground='#2C4C71')
    purchase_frame.grid(row=0, column=0, sticky=NW)
    purchase_frame.propagate(0)
    purchase_frame.update()

    Label(
        purchase_frame,
        text='购买项目',
        font='Arial 18 bold').place(
            relx=.5,
            y=40,
            anchor=CENTER)
    Button(
        purchase_frame,
        text='返回',
        command=purchase_back,
        height=2,
        width=5,
        background='#2C4C71',
        foreground='#E9EEF3').place(
            relx=.04,
            y=40,
            anchor=CENTER)
    purchase_searchentry = Entry(
        purchase_frame,
        width=20,
        textvariable=purchaseinput_search,
        font='Arial 8',
        foreground='black',
        highlightthickness=1,
        highlightbackground='#2C4C71',
        highlightcolor='#2C4C71')
    purchase_searchbutton = Button(
        purchase_frame,
        text='搜索',
        command=purchase_searchitem,
        height=1,
        width=5,
        background='#2C4C71',
        foreground='#E9EEF3')
    purchase_itemnamelabel = Label(
        purchase_frame,
        text='项目名',
        font='Arial 8')
    purchase_itemnameentry = Entry(
        purchase_frame,
        width=30,
        textvariable=purchaseinput_itemname,
        font='Arial 8',
        state=DISABLED)
    purchase_quantitylabel = Label(
        purchase_frame,
        text='库存',
        font='Arial 8')
    purchase_quantityentry = Entry(
        purchase_frame,
        width=10,
        textvariable=purchaseinput_quantity,
        font='Arial 8')
    purchase_addbutton = Button(
        purchase_frame,
        text='添加',
        command=purchase_additem,
        state=DISABLED,
        height=1,
        width=5,
        background='#2C4C71',
        foreground='#E9EEF3')
    purchase_removebutton = Button(
        purchase_frame,
        text='移除',
        command=purchase_removeitem,
        state=DISABLED,
        height=1,
        width=8,
        background='#2C4C71',
        foreground='#E9EEF3')
    purchase_checkoutbutton = Button(
        purchase_frame,
        text='结账',
        command=purchase_checkoutitems,
        state=DISABLED,
        height=1,
        width=8,
        background='#2C4C71',
        foreground='#E9EEF3')
    purchase_totallabel = Label(
        purchase_frame,
        textvariable=purchase_carttotal,
        font='Arial 14 bold')

    cols = ('项目名', '库存', '价格')
    purchase_treeview = ttk.Treeview(
        purchase_frame, columns=cols, show='headings')

    invItems = getInvItems()
    if len(invItems) == 0:
        purchase_treeview.unbind('<ButtonRelease-1>')
        purchase_searchentry.config(state='disabled')
        purchase_searchbutton.config(state='disabled')
        purchase_quantityentry.config(state='disabled')
        purchase_addbutton.config(state='disabled')
        messagebox.showinfo('信息', '仓库里没有相关项目')
    else:
        purchase_treeview.bind('<ButtonRelease-1>', purchase_binditem)

    for col in cols:
        purchase_treeview.heading(col, text=col)
        purchase_treeview.grid(row=1, column=0, columnspan=2)
        purchase_treeview.column(col, anchor=CENTER)
        purchase_treeview.place(relx=.5, rely=.4, anchor=CENTER)

    tempInvList = []
    for key, value in getInvItems().items():
        tempInvList.append([key, value[0]['quantity'], value[1]['price']])
    tempInvList.sort(key=lambda x: x[2])
    for i in enumerate(tempInvList, start=1):
        purchase_treeview.insert('', 'end', values=(i[1][0], i[1][1], i[1][2]))

    purchase_searchentry.place(x=165, y=110, anchor=CENTER)
    purchase_searchbutton.place(x=250, y=110, anchor=CENTER)

    purchase_itemnamelabel.place(x=180, y=360)
    purchase_itemnameentry.place(x=180, y=380)
    purchase_quantitylabel.place(x=420, y=360)
    purchase_quantityentry.place(x=420, y=380)
    purchase_addbutton.place(x=530, y=370)

    cart_cols = ('项目名', '库存', '小计')
    purchase_carttreeview = ttk.Treeview(
        purchase_frame, columns=cart_cols, show='headings', height=6)

    if len(invItems) == 0:
        purchase_carttreeview.unbind('<ButtonRelease-1>')
        purchase_removebutton.config(state='disabled')
        purchase_checkoutbutton.config(state='disabled')
    else:
        purchase_carttreeview.bind('<ButtonRelease-1>', purchase_bindcartitem)

    for col in cart_cols:
        purchase_carttreeview.heading(col, text=col)
        purchase_carttreeview.grid(row=1, column=0, columnspan=2)
        purchase_carttreeview.column(col, anchor=CENTER)
        purchase_carttreeview.place(x=100, y=410)
    purchase_carttreeview.column('#1', anchor=CENTER, width=200)
    purchase_carttreeview.column('#2', anchor=CENTER, width=80)
    purchase_carttreeview.column('#3', anchor=CENTER, width=120)

    purchase_removebutton.place(x=530, y=440)
    purchase_checkoutbutton.place(x=530, y=470)
    purchase_totallabel.place(x=530, y=500)
    purchase_carttotal.set('总计: ￥0.00')


def login():
    def judge(event=None):
        if acc.get() != 'admin' or pwd.get() != 'password':
            messagebox.showerror('*_*', '账号或密码错误,请重新输入')
        else:
            messagebox.showinfo('^_^', '管理员账号登录成功')
            global signed
            signed = True
            enter_w.destroy()

    if not signed:
        enter_w = Tk()
        enter_w.title('Log in')
        enter_w.geometry('300x150')
        enter_w.attributes('-topmost', 'true')

        # 回车登录
        enter_w.bind('<Key-Return>', judge)

        lab_1 = Label(enter_w, width=7, text='用户名', compound='center')
        lab_1.place(x=30, y=20)

        lab_2 = Label(enter_w, width=7, text='密码', compound='center')
        lab_2.place(x=30, y=60)
        user_name = StringVar()
        password = StringVar()

        acc = Entry(enter_w, textvariable=user_name)
        acc.pack()
        acc.place(x=100, y=20)

        pwd = Entry(enter_w, show="*", textvariable=password)
        pwd.pack()
        pwd.place(x=100, y=60)

        btn = Button(enter_w, text='登录', fg="black", width=7,
                     compound='center', bg="white", command=judge)
        btn.pack()
        btn.place(x=120, y=100)
        enter_w.mainloop()
    else:
        messagebox.showinfo("提示", "您已登录，请勿重复操作！")


def logout():
    global signed
    if signed:
        confirm = messagebox.askyesno("确认", "您确认退出管理员账号吗？")
        if confirm:
            signed = False
        else:
            pass
    else:
        messagebox.showwarning("错误", "傻子！你还没登录过呢！")


def main_window():
    main_frame = Frame(window, width=800, height=600)
    main_frame.tk_setPalette(background='#446285', foreground='#A5B8CC')
    main_frame.grid(row=0, column=0, sticky=NW)
    main_frame.grid_propagate(0)
    main_frame.update()

    menubar = Menu(window)
    adminmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='管理员', menu=adminmenu)
    adminmenu.add_command(label='登录', command=login)
    adminmenu.add_command(label='登出', command=logout)

    window.config(menu=menubar)

    Label(
        main_frame,
        text='售货和仓库系统',
        font='Arial 18 bold').place(relx=.5,
                                    y=40,
                                    anchor=CENTER)
    Button(
        main_frame,
        text='添加项目',
        command=add_window,
        height=8,
        width=30,
        background='#A5B8CC',
        foreground='black').place(
            relx=.5,
            y=190,
            anchor=CENTER)
    Button(
        main_frame,
        text='浏览项目',
        command=view_window,
        height=8,
        width=30,
        background='#A5B8CC',
        foreground='black').place(
            relx=.5,
            y=340,
            anchor=CENTER)
    Button(
        main_frame,
        text='购买项目',
        command=purchase_window,
        height=8,
        width=30,
        background='#A5B8CC',
        foreground='black').place(
            relx=.5,
            y=490,
            anchor=CENTER)


if __name__ == '__main__':
    main_window()
    window.mainloop()
