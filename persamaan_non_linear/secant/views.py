from django.shortcuts import render
import plotly.graph_objs as go
import plotly.io as pio
import sympy as sp

# Fungsi Metode Secant
def metode_secant(f_expr, x0, x1, tol, max_iter):
    """
    Fungsi untuk menghitung akar dari sebuah fungsi menggunakan metode secant.

    Parameters:
    f_expr (str): Ekspresi fungsi sebagai string.
    x0, x1 (float): Pendekatan awal.
    tol (float): Toleransi error yang diizinkan.
    max_iter (int): Jumlah iterasi maksimum.

    Returns:
    tuple: List dari setiap iterasi yang mencakup nilai x, f(x), serta pesan error jika ada.
    """
    x = sp.symbols('x')
    f = sp.sympify(f_expr, locals={'e': sp.exp(1)})  # Mengubah string menjadi ekspresi
    f_lambdified = sp.lambdify(x, f)

    iterations = []
    for i in range(max_iter):
        f_x0 = f_lambdified(x0)
        f_x1 = f_lambdified(x1)

        # Cek apakah denominasi nol untuk menghindari error pembagian dengan nol
        if (f_x1 - f_x0) == 0:
            return None, "Pembagian dengan nol, metode secant gagal."

        # Mencari nilai baru untuk x menggunakan rumus metode secant
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # Menyimpan hasil iterasi
        status = "Lanjut" if abs(f_x1) >= tol else "Berhenti"
        iterations.append({
            'iteration': i + 1,
            'x0': x0,
            'x1': x1,
            'f_x0': f_x0,
            'f_x1': f_x1,
            'status': status,
        })

         # Cek apakah nilai f_x1 mendekati nol
        if abs(f_x1) < tol:
            break

        # Update nilai untuk iterasi berikutnya
        x0, x1 = x1, x2
    print(iterations)
    return iterations, None

def index(req):
    """
    Fungsi view untuk menangani permintaan halaman utama dan menghitung akar menggunakan metode secant.

    Parameters:
    request (HttpRequest): Objek permintaan dari pengguna.

    Returns:
    HttpResponse: Halaman HTML yang dirender.
    """
    result = None
    error_message = None
    plot_div = None

    if req.method == 'POST':
        try:
            # Mengambil input dari pengguna
            f_expr = req.POST.get('f_expr')
            x0 = float(req.POST.get('x0'))
            x1 = float(req.POST.get('x1'))
            tol = float(req.POST.get('tol'))
            max_iter = int(req.POST.get('max_iter'))

            # Jalankan metode Secant
            result, error_message = metode_secant(f_expr, x0, x1, tol, max_iter)

            # Membuat grafik menggunakan Plotly jika hasil ada hasil
            if result:
                # Membuat data yang akan digunakan untuk membuat plot
                x_values = [info['iteration'] for info in result]
                y_values = [info['f_x1'] for info in result]

                trace = go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines+markers',
                    name='f(x)',
                    line=dict(color='royalblue', width=2),
                    marker=dict(size=6)
                )

                layout = go.Layout(
                    title='Grafik Konvergensi Metode Secant',
                    xaxis=dict(title='Iterasi'),
                    yaxis=dict(title='f(x)'),
                    template='plotly_white'
                )

                fig = go.Figure(data=[trace], layout=layout)
                plot_div = pio.to_html(fig, full_html=False)

        except ValueError:
            error_message = "Masukan nilai numerik yang valid kkk."
        except (SyntaxError, NameError):
            error_message = "Masukan fungsi ekspresi yang valid."

    return render(req, 'secant/pages/index.html', {
        'result': result,
        'error_message': error_message,
        'plot_div': plot_div,
        'f_expr': req.POST.get('f_expr'),
        'x0': req.POST.get('x0'),
        'x1': req.POST.get('x1'),
        'tol': req.POST.get('tol'),
        'max_iter': req.POST.get('max_iter')
    })
