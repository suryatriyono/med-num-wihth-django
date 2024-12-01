from django.shortcuts import render
import plotly.graph_objs as go
import plotly.io as pio
import json
import math


# Fungsi regulasi falsi
def regula_falsi(f, a, b, tol, max_iter):
    """
    Fungsi untuk menghitung akar dari sebuah fungsi menggunakan metode Regula Falsi.

    Parameters:
    f (function): Fungsi yang akan dicari akarnya.
    a (float): Batas bawah interval.
    b (float): Batas atas interval.
    tol (float): Toleransi error yang diizinkan.
    max_iter (int): Jumlah iterasi maksimum.

    Returns:
    tuple: List dari setiap iterasi yang mencakup nilai a, b, xr, dan f(xr), serta pesan error jika ada.
    """
    # Jika f(a) dan f(b) memiliki tanda yang sama, akar tidak mungkin ada di interval tersebut
    if f(a) * f(b) >= 0:
        return None, "Interval [a, b] tidak mengandung akar."

    iterations = []
    xr = a  # Inisialisasi nilai xr
    for i in range(max_iter):
        # Menghitung nilai xr menggunakan rumus Regula Falsi
        xr = b - (f(b) * (a - b)) / (f(a) - f(b))
        fxr = f(xr)  # Menghitung nilai f(xr)

        # Menyimpan informasi iterasi ke dalam list iterations
        iterations.append({
            'iteration': i + 1,
            'a': a,
            'b': b,
            'xr': xr,
            'f_xr': fxr
        })

        # Memeriksa apakah nilai f(xr) sudah mendekati nol dalam toleransi error yang ditentukan
        if abs(fxr) < tol:
            break

        # Menentukan interval baru berdasarkan tanda dari f(a) dan f(xr)
        if f(a) * fxr < 0:
            b = xr  # Akar berada di interval [a, xr]
        else:
            a = xr  # Akar berada di interval [xr, b]

    return iterations, None

# Fungsi view untuk form dan hasil
def index(request):
    """
    Fungsi view untuk menangani permintaan halaman utama dan menghitung akar menggunakan metode Regula Falsi.

    Parameters:
    request (HttpRequest): Objek permintaan dari pengguna.

    Returns:
    HttpResponse: Halaman HTML yang dirender.
    """
    result = None
    error_message = None
    plot_div = None
    if request.method == 'POST':
        try:
            # Mengambil input dari pengguna
            a = float(request.POST.get('a'))
            b = float(request.POST.get('b'))
            tol = float(request.POST.get('tol'))
            max_iter = int(request.POST.get('max_iter'))
            f_expression = request.POST.get('f_expression')

            # Mendefinisikan fungsi f(x) berdasarkan input pengguna
            def f(x):
                return eval(f_expression)

            # Jalankan metode Regula Falsi dengan parameter yang diberikan
            result, error_message = regula_falsi(f, a, b, tol, max_iter)

            # Membuat grafik menggunakan Plotly jika hasil ada
            if result:
                x_values = [r['iteration'] for r in result]
                y_values = [r['f_xr'] for r in result]

                trace = go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines+markers',
                    name='f(xr)',
                    line=dict(color='royalblue', width=2),
                    marker=dict(size=6)
                )

                layout = go.Layout(
                    title='Grafik Konvergensi Metode Regula Falsi',
                    xaxis=dict(title='Iterasi'),
                    yaxis=dict(title='f(xr)'),
                    template='plotly_white'
                )

                fig = go.Figure(data=[trace], layout=layout)
                plot_div = pio.to_html(fig, full_html=False)

        except ValueError:
            error_message = "Masukkan nilai numerik yang valid."
        except (SyntaxError, NameError):
            error_message = "Masukkan ekspresi fungsi yang valid."

    # Merender halaman dengan hasil atau pesan error jika ada
    return render(request, 'pages/index.html', {
        'result': result,
        'error_message': error_message,
        'plot_div': plot_div
    })

















# from django.shortcuts import render
# import math
# import matplotlib.pyplot as plt
# import io
# import urllib, base64

# # Fungsi regulasi falsi
# def regula_falsi(f, a, b, tol, max_iter):
#     """
#     Fungsi untuk menghitung akar dari sebuah fungsi menggunakan metode Regula Falsi.

#     Parameters:
#     f (function): Fungsi yang akan dicari akarnya.
#     a (float): Batas bawah interval.
#     b (float): Batas atas interval.
#     tol (float): Toleransi error yang diizinkan.
#     max_iter (int): Jumlah iterasi maksimum.

#     Returns:
#     tuple: List dari setiap iterasi yang mencakup nilai a, b, xr, dan f(xr), serta pesan error jika ada.
#     """
#     # Jika f(a) dan f(b) memiliki tanda yang sama, akar tidak mungkin ada di interval tersebut
#     if f(a) * f(b) >= 0:
#         return None, "Interval [a, b] tidak mengandung akar."

#     iterations = []
#     xr = a  # Inisialisasi nilai xr
#     for i in range(max_iter):
#         # Menghitung nilai xr menggunakan rumus Regula Falsi
#         xr = b - (f(b) * (a - b)) / (f(a) - f(b))
#         fxr = f(xr)  # Menghitung nilai f(xr)

#         # Menyimpan informasi iterasi ke dalam list iterations
#         iterations.append({
#             'iteration': i + 1,
#             'a': a,
#             'b': b,
#             'xr': xr,
#             'f_xr': fxr
#         })

#         # Memeriksa apakah nilai f(xr) sudah mendekati nol dalam toleransi error yang ditentukan
#         if abs(fxr) < tol:
#             break

#         # Menentukan interval baru berdasarkan tanda dari f(a) dan f(xr)
#         if f(a) * fxr < 0:
#             b = xr  # Akar berada di interval [a, xr]
#         else:
#             a = xr  # Akar berada di interval [xr, b]

#     return iterations, None

# # Fungsi view untuk form dan hasil
# def index(request):
#     """
#     Fungsi view untuk menangani permintaan halaman utama dan menghitung akar menggunakan metode Regula Falsi.

#     Parameters:
#     request (HttpRequest): Objek permintaan dari pengguna.

#     Returns:
#     HttpResponse: Halaman HTML yang dirender.
#     """
#     result = None
#     error_message = None
#     plot_div = None
#     if request.method == 'POST':
#         try:
#             # Mengambil input dari pengguna
#             a = float(request.POST.get('a'))
#             b = float(request.POST.get('b'))
#             tol = float(request.POST.get('tol'))
#             max_iter = int(request.POST.get('max_iter'))
#             f_expression = request.POST.get('f_expression')

#             # Mendefinisikan fungsi f(x) berdasarkan input pengguna
#             def f(x):
#                 return eval(f_expression)

#             # Jalankan metode Regula Falsi dengan parameter yang diberikan
#             result, error_message = regula_falsi(f, a, b, tol, max_iter)

#             if result:
#                 x_values = [r['xr'] for r in result]
#                 y_values = [r['f_xr'] for r in result]

#                 plt.figure(figsize=(10, 5))
#                 plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
#                 plt.xlabel('xr (Perkiraan Akar)')
#                 plt.ylabel('f(xr)')
#                 plt.title('Konvergensi Metode Regula Falsi')
#                 plt.grid(True)

#                 # Simpan grafik ke buffer dalam format PNG
#                 buf = io.BytesIO()
#                 plt.savefig(buf, format='png')
#                 buf.seek(0)
#                 string = base64.b64encode(buf.read())
#                 plot_div = 'data:image/png;base64,' + urllib.parse.quote(string)

#         except ValueError:
#             error_message = "Masukkan nilai numerik yang valid."
#         except (SyntaxError, NameError):
#             error_message = "Masukkan ekspresi fungsi yang valid."

#     # Merender halaman dengan hasil atau pesan error jika ada
#     return render(request, 'pages/index.html', {
#         'result': result,
#         'error_message': error_message,
#         'plot_div': plot_div
#     })