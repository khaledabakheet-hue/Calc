import tkinter as tk
from tkinter import messagebox

# المتغيرات العامة
current_input = ""
result_var = None
history = []

def create_calculator():
    """إنشاء واجهة الآلة الحاسبة"""
    root = tk.Tk()
    root.title("🧮 الآلة الحاسبة البسيطة")
    root.geometry("300x450")
    root.resizable(False, False)
    
    global result_var
    result_var = tk.StringVar()
    result_var.set("0")
    
    # إنشاء عناصر الواجهة
    create_widgets(root)
    
    return root

def create_widgets(root):
    """إنشاء عناصر الواجهة"""
    # شاشة العرض
    display = tk.Entry(
        root,
        textvariable=result_var,
        font=('Arial', 20),
        justify='right',
        state='readonly',
        bg='#f0f0f0',
        bd=10
    )
    display.pack(fill=tk.X, padx=10, pady=10, ipady=10)
    
    # إطار الأزرار
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    # تخطيط الأزرار
    buttons = [
        ['C', '⌫', '%', '/'],
        ['7', '8', '9', '*'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['0', '.', '=', '±']
    ]
    
    # إنشاء الأزرار
    for i, row in enumerate(buttons):
        for j, text in enumerate(row):
            # تحديد ألوان الأزرار
            if text in ['/', '*', '-', '+', '=']:
                bg_color = '#ff9500'
                fg_color = 'white'
            elif text in ['C', '⌫', '%', '±']:
                bg_color = '#a6a6a6'
                fg_color = 'black'
            else:
                bg_color = '#333333'
                fg_color = 'white'
            
            # تحديد عرض الزر الخاص بـ 0
            if text == '0':
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=('Arial', 16, 'bold'),
                    bg=bg_color,
                    fg=fg_color,
                    relief='raised',
                    bd=3,
                    command=lambda t=text: button_click(t)
                )
                btn.grid(row=i, column=j, columnspan=2, sticky='ew', padx=2, pady=2)
            else:
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=('Arial', 16, 'bold'),
                    bg=bg_color,
                    fg=fg_color,
                    relief='raised',
                    bd=3,
                    command=lambda t=text: button_click(t)
                )
                btn.grid(row=i, column=j, sticky='ew', padx=2, pady=2)
    
    # تكبير أعمدة الإطار
    for i in range(4):
        buttons_frame.columnconfigure(i, weight=1)
    for i in range(5):
        buttons_frame.rowconfigure(i, weight=1)
    
    # زر عرض السجل
    history_btn = tk.Button(
        root,
        text="📋 عرض السجل",
        font=('Arial', 12),
        bg='#4CAF50',
        fg='white',
        command=show_history
    )
    history_btn.pack(fill=tk.X, padx=10, pady=5)

def button_click(value):
    """معالجة النقر على الأزرار"""
    global current_input
    
    try:
        if value.isdigit() or value == '.':
            input_number(value)
        elif value in ['+', '-', '*', '/']:
            input_operator(value)
        elif value == '=':
            calculate()
        elif value == 'C':
            clear_all()
        elif value == '⌫':
            backspace()
        elif value == '±':
            toggle_sign()
        elif value == '%':
            percentage()
    except Exception as e:
        show_error("خطأ في العملية الحسابية")

def input_number(num):
    """إدخال رقم أو نقطة عشرية"""
    global current_input
    
    if current_input == "0" or current_input == "خطأ":
        current_input = ""
    
    if num == '.' and '.' in current_input:
        return  # منع إضافة أكثر من نقطة عشرية
    
    current_input += num
    result_var.set(current_input)

def input_operator(op):
    """إدخال عامل حسابي"""
    global current_input
    
    if current_input and current_input != "خطأ":
        # إذا كان هناك عملية سابقة، احسبها أولاً
        if any(x in current_input for x in ['+', '-', '*', '/']):
            calculate()
        
        current_input += f" {op} "
        result_var.set(current_input)

def calculate():
    """إجراء العملية الحسابية"""
    global current_input
    
    try:
        if not current_input or current_input == "خطأ":
            return
        
        # تنظيف المدخلات
        expression = current_input.replace(' ', '')
        
        # التحقق من أن العملية تحتوي على معاملين
        if any(op in expression for op in ['+', '-', '*', '/']):
            # فصل الأرقام والعوامل
            if '+' in expression:
                parts = expression.split('+')
                if len(parts) == 2:
                    result = float(parts[0]) + float(parts[1])
            elif '-' in expression:
                parts = expression.split('-')
                if len(parts) == 2:
                    result = float(parts[0]) - float(parts[1])
            elif '*' in expression:
                parts = expression.split('*')
                if len(parts) == 2:
                    result = float(parts[0]) * float(parts[1])
            elif '/' in expression:
                parts = expression.split('/')
                if len(parts) == 2:
                    if float(parts[1]) == 0:
                        raise ZeroDivisionError("القسمة على صفر")
                    result = float(parts[0]) / float(parts[1])
            
            # حفظ في السجل
            history.append(f"{current_input} = {result}")
            
            # عرض النتيجة
            current_input = str(result)
            result_var.set(current_input)
            
    except ZeroDivisionError:
        show_error("لا يمكن القسمة على صفر!")
        current_input = ""
        result_var.set("خطأ")
    except ValueError:
        show_error("مدخل غير صحيح")
        current_input = ""
        result_var.set("خطأ")
    except Exception as e:
        show_error("خطأ في الحساب")
        current_input = ""
        result_var.set("خطأ")

def clear_all():
    """مسح الكل"""
    global current_input
    current_input = ""
    result_var.set("0")

def backspace():
    """حذف آخر مدخل"""
    global current_input
    
    if current_input and current_input != "خطأ":
        current_input = current_input[:-1]
        if not current_input:
            result_var.set("0")
        else:
            result_var.set(current_input)

def toggle_sign():
    """تبديل الإشارة"""
    global current_input
    
    if current_input and current_input != "خطأ":
        if current_input.startswith('-'):
            current_input = current_input[1:]
        else:
            current_input = '-' + current_input
        result_var.set(current_input)

def percentage():
    """حساب النسبة المئوية"""
    global current_input
    
    try:
        if current_input and current_input != "خطأ":
            value = float(current_input)
            result = value / 100
            current_input = str(result)
            result_var.set(current_input)
    except:
        show_error("خطأ في حساب النسبة")

def show_history():
    """عرض سجل العمليات"""
    if not history:
        messagebox.showinfo("السجل", "لا توجد عمليات سابقة")
        return
    
    history_text = "\n".join(history[-10:])  # آخر 10 عمليات
    messagebox.showinfo("سجل العمليات", history_text)

def show_error(message):
    """عرض رسالة خطأ"""
    messagebox.showerror("خطأ", message)

def main():
    """الدالة الرئيسية"""
    root = create_calculator()
    root.mainloop()

if __name__ == "__main__":
    main()