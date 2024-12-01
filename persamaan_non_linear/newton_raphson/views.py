from django.shortcuts import render
import plotly.graph_objs as go
import plotly.io as pio
import math
import sympy as sp
import json

# Fungsi Newton Rapshon
def newton_rapshon(f_expr, x0, tol, max_iter):
    """
    Fungsi untuk menghitung akar dari sebuah fungsi menggunakan metode Newton Raphson.

    Parameters:
    f_expr (str): Ekspresi fungsi sebagai string.
    x0 (float): Pendekatan awal.
    tol (float): Toleransi error yang diizinkan.
    max_iter (int): Jumlah iterasi maksimum.

    Returns:
    tuple: List dari setiap iterasi yang mencakup nilai x, f(x), f'(x), serta pesan error jika ada.
    """
    x = sp.symbols('x')
    f = sp.sympify(f_expr, locals={'e': sp.exp(1)}) # Mengubah string menjadi ekspresi
    f_prime = sp.diff(f, x)  # Menghitung turuan pertama dari f

    # Mendefenisikan fungsi f(x) dan f'(x)
    f_lambdified = sp.lambdify(x,f)
    f_prime_lambdified = sp.lambdify(x, f_prime) 

    interatios = []
    xi = x0
    for i in range(max_iter):
        fxi = f_lambdified(xi)
        f_prime_xi = f_prime_lambdified(xi)

        # Cek apakah f'(x) = 0
        if f_prime_xi == 0:
            return None, "Turunan mendekati nol, metode Newton-Raphson gagal."
            
        # menyimpan informasi itersi ke dalam iterations
        status = "Lanjut" if abs(fxi) >= tol else "Berhenti"
        interatios.append({
            'iteration': i + 1,
            'x': xi,
            'f_x': fxi,
            'f_prime_x': f_prime_xi,
            'status': status,
        })

        # Memerisa apakah nilai f(xi) sudah mendekati nol dalam teleransi error yang ditentukan
        if abs(fxi) < tol:
            break

        # Mencari akar berikutnya menggunakan metode Newton-Raphson
        xi = xi - fxi / f_prime_xi
    return interatios, None, f_prime



def index(req):
    """
    Fungsi view untuk menangani permintaan halaman utama dan menghitung akar menggunakan metode Newton Raphson.

    Parameters:
    request (HttpRequest): Objek permintaan dari pengguna.

    Returns:
    HttpResponse: Halaman HTML yang dirender.
    """
    result = None
    error_message = None
    plot_div = None
    f_prime_res = None

    if req.method == 'POST':
        try:
            # Mengambil input dari pengguna
            f_expr = req.POST.get('f_expr')
            x0 = float(req.POST.get('x'))
            tol = float(req.POST.get('tol'))
            max_iter = int(req.POST.get('max_iter'))

            # Jalankan method Newton Rapshon
            result, error_message, f_prime_res = newton_rapshon(f_expr, x0, tol, max_iter)

            # Membuat grafik menggunkan Ploty jika hasil ada hasil
            if result:
                # Membuat data yang akan digunakan untuk membuat plot
                x_values = [info['iteration'] for info in result]
                y_values = [info['f_x'] for info in result]

                trace = go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines+markers',
                    name='f(x)',
                    line=dict(color='royalblue', width=2),
                    marker=dict(size=6)
                )

                layout = go.Layout(
                    title='Grafik Konvergensi Metode Newton Raphson',
                    xaxis=dict(title='Iterasi'),
                    yaxis=dict(title='f(x)'),
                    template='plotly_white'
                )

                fig = go.Figure(data=[trace], layout=layout)
                plot_div = pio.to_html(fig, full_html=False)
            
        except ValueError:
            error_message = "Masukan nilai numerik yang valid"
        except(SyntaxError, NameError):
            error_message = "Masukan fungsi ekpsresi yang valid"

    return render(req, 'pages/index.html', {
        'result': result,
        'error_message': error_message,
        'plot_div': plot_div,
        'f_prime': f_prime_res,
        'f_expr': req.POST.get('f_expr'),
        'x' : req.POST.get('x'),
        'tol' : req.POST.get('tol'),
        'max_iter' : req.POST.get('max_iter')
    })

