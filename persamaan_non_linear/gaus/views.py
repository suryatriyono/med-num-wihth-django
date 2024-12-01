from django.shortcuts import render
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
import ast  # Digunakan untuk parsing input yang aman

# Fungsi Metode Eliminasi Gauss
def eliminasi_gauss(matrix, results):
    # Mengubah matriks input dan hasil menjadi matriks augmented
    augmented_matrix = np.array(matrix, dtype=float)
    results_vector = np.array(results, dtype=float).reshape(-1, 1)
    augmented_matrix = np.hstack((augmented_matrix, results_vector))
    n = len(results)

    steps = []  # Untuk menyimpan langkah-langkah eliminasi
    descriptions = []  # Untuk menyimpan deskripsi langkah

    # Forward Elimination
    for i in range(n):
        # Pivoting jika elemen diagonal utama adalah nol
        if augmented_matrix[i, i] == 0:
            for k in range(i + 1, n):
                if augmented_matrix[k, i] != 0:
                    augmented_matrix[[i, k]] = augmented_matrix[[k, i]]
                    descriptions.append(f"Menukar baris {i + 1} dengan baris {k + 1} karena elemen pivot bernilai nol.")
                    break
            else:
                return None, "Tidak ada solusi unik."
        
        # Normalisasi baris pivot
        pivot_value = augmented_matrix[i, i]
        augmented_matrix[i] = augmented_matrix[i] / pivot_value
        descriptions.append(f"Normalisasi baris {i + 1} dengan membagi semua elemen dengan {int(pivot_value) if pivot_value.is_integer() else pivot_value}.")
        steps.append(augmented_matrix.copy())

        # Eliminasi untuk membuat nol di bawah elemen pivot
        for j in range(i + 1, n):
            factor = augmented_matrix[j, i]
            augmented_matrix[j] = augmented_matrix[j] - factor * augmented_matrix[i]
            descriptions.append(f"Mengurangi baris {j + 1} dengan baris {i + 1} dikalikan {int(factor) if factor.is_integer() else factor} untuk membuat elemen di bawah pivot menjadi nol.")
            steps.append(augmented_matrix.copy())

    # Back Substitution
    x = np.zeros(n)
    back_sub_steps = []  # Untuk menyimpan langkah back substitution dengan detail persamaan
    for i in range(n - 1, -1, -1):
        sum_ax = np.sum(augmented_matrix[i, i + 1:n] * x[i + 1:n])
        x[i] = augmented_matrix[i, -1] - sum_ax
        equation = " + ".join([f"{augmented_matrix[i, j]}*x{j + 1}" for j in range(i + 1, n) if augmented_matrix[i, j] != 0])
        if equation:
            equation = f"{augmented_matrix[i, i]}*x{i + 1} + {equation} = {augmented_matrix[i, -1]}"
        else:
            equation = f"{augmented_matrix[i, i]}*x{i + 1} = {augmented_matrix[i, -1]}"
        variable_name = chr(120 + i)  # Menggunakan ASCII untuk mendapatkan nama variabel (x, y, z, dst.)
        back_sub_steps.append(f"{equation}\n   {variable_name} = {x[i]}")
        descriptions.append(f"Melakukan substitusi balik untuk menghitung nilai {variable_name}.")

    # Mengganti nilai -0.0 dengan 0.0 untuk kejelasan di augmented matrix dan hasil
    augmented_matrix[augmented_matrix == -0.0] = 0.0
    x[x == -0.0] = 0.0

    return steps, descriptions, x, back_sub_steps


def index(req):
    """
    Fungsi view untuk menangani permintaan halaman utama dan menghitung sistem persamaan linear menggunakan metode eliminasi Gauss.
    
    Mengambil input dari pengguna, menjalankan metode eliminasi Gauss, dan mengembalikan hasil serta langkah-langkah perhitungan.
    """
    result = None
    error_message = None
    steps = []
    descriptions = []
    plot_div = None
    combined_steps = []
    back_sub_steps = []

    if req.method == 'POST':
        try:
            # Mengambil input dari pengguna dan parsing menggunakan ast.literal_eval untuk keamanan
            matrix = req.POST.get('matrix')  # Input matriks dalam bentuk string
            results = req.POST.get('results')  # Input hasil dalam bentuk string

            # Menggunakan ast.literal_eval untuk parsing input secara aman
            matrix = ast.literal_eval(matrix)  # Menghindari penggunaan eval() yang tidak aman
            results = ast.literal_eval(results)

            # Jalankan metode eliminasi Gauss
            steps, descriptions, result, back_sub_steps = eliminasi_gauss(matrix, results)
            combined_steps = list(zip(steps, descriptions))

            # Membuat grafik menggunakan Plotly jika terdapat langkah eliminasi
            if steps:
                traces = []
                for step_idx, step in enumerate(steps):
                    # Membuat heatmap dari setiap langkah eliminasi
                    trace = go.Heatmap(z=step, coloraxis="coloraxis", name=f'Step {step_idx + 1}')
                    traces.append(trace)

                layout = go.Layout(
                    title='Proses Eliminasi Gauss',
                    xaxis=dict(title='Kolom'),
                    yaxis=dict(title='Baris'),
                    template='plotly_white',
                    coloraxis=dict(colorscale='Viridis')
                )

                fig = go.Figure(data=traces, layout=layout)
                plot_div = pio.to_html(fig, full_html=False)

        except ValueError:
            error_message = "Masukkan nilai numerik yang valid."
        except (SyntaxError, NameError):
            error_message = "Masukkan input matriks dan hasil yang valid."

    return render(req, 'gaus/pages/index.html', {
        'result': result,
        'steps': steps,
        'descriptions': descriptions,
        'error_message': error_message,
        'plot_div': plot_div,
        'matrix': req.POST.get('matrix'),
        'results': req.POST.get('results'),
        'combined_steps': combined_steps,
        'back_sub_steps': back_sub_steps,
    })









# from django.shortcuts import render
# import plotly.graph_objs as go
# import plotly.io as pio
# import numpy as np
# import ast  # Digunakan untuk parsing input yang aman

# # Fungsi Metode Eliminasi Gauss
# def eliminasi_gauss(matrix, results):
#     # Mengubah matriks input dan hasil menjadi matriks augmented
#     augmented_matrix = np.array(matrix, dtype=float)
#     results_vector = np.array(results, dtype=float).reshape(-1, 1)
#     augmented_matrix = np.hstack((augmented_matrix, results_vector))
#     n = len(results)

#     steps = []  # Untuk menyimpan langkah-langkah eliminasi
#     descriptions = []  # Untuk menyimpan deskripsi langkah

#     # Forward Elimination
#     for i in range(n):
#         # Pivoting jika elemen diagonal utama adalah nol
#         if augmented_matrix[i, i] == 0:
#             for k in range(i + 1, n):
#                 if augmented_matrix[k, i] != 0:
#                     augmented_matrix[[i, k]] = augmented_matrix[[k, i]]
#                     descriptions.append(f"Menukar baris {i + 1} dengan baris {k + 1} karena elemen pivot bernilai nol.")
#                     break
#             else:
#                 return None, "Tidak ada solusi unik."
        
#         # Normalisasi baris pivot
#         pivot_value = augmented_matrix[i, i]
#         augmented_matrix[i] = augmented_matrix[i] / pivot_value
#         descriptions.append(f"Normalisasi baris {i + 1} dengan membagi semua elemen dengan {int(pivot_value) if pivot_value.is_integer() else pivot_value}.")
#         steps.append(augmented_matrix.copy())

#         # Eliminasi untuk membuat nol di bawah elemen pivot
#         for j in range(i + 1, n):
#             factor = augmented_matrix[j, i]
#             augmented_matrix[j] = augmented_matrix[j] - factor * augmented_matrix[i]
#             descriptions.append(f"Mengurangi baris {j + 1} dengan baris {i + 1} dikalikan {int(factor) if factor.is_integer() else factor} untuk membuat elemen di bawah pivot menjadi nol.")
#             steps.append(augmented_matrix.copy())

#     # Back Substitution
#     x = np.zeros(n)
#     back_sub_steps = []  # Untuk menyimpan langkah back substitution dengan detail persamaan
#     for i in range(n - 1, -1, -1):
#         sum_ax = np.sum(augmented_matrix[i, i + 1:n] * x[i + 1:n])
#         x[i] = augmented_matrix[i, -1] - sum_ax
#         equation = " + ".join([f"{augmented_matrix[i, j]}*x{j + 1}" for j in range(i + 1, n) if augmented_matrix[i, j] != 0])
#         if equation:
#             equation = f"{augmented_matrix[i, i]}*x{i + 1} + {equation} = {augmented_matrix[i, -1]}"
#         else:
#             equation = f"{augmented_matrix[i, i]}*x{i + 1} = {augmented_matrix[i, -1]}"
#         back_sub_steps.append(f"{equation}\n   x{i + 1} = {x[i]}")
#         descriptions.append(f"Melakukan substitusi balik untuk menghitung nilai x{i + 1}.")

#     # Mengganti nilai -0.0 dengan 0.0 untuk kejelasan di augmented matrix dan hasil
#     augmented_matrix[augmented_matrix == -0.0] = 0.0
#     x[x == -0.0] = 0.0

#     return steps, descriptions, x, back_sub_steps


# def index(req):
#     """
#     Fungsi view untuk menangani permintaan halaman utama dan menghitung sistem persamaan linear menggunakan metode eliminasi Gauss.
    
#     Mengambil input dari pengguna, menjalankan metode eliminasi Gauss, dan mengembalikan hasil serta langkah-langkah perhitungan.
#     """
#     result = None
#     error_message = None
#     steps = []
#     descriptions = []
#     plot_div = None
#     combined_steps = []
#     back_sub_steps = []

#     if req.method == 'POST':
#         try:
#             # Mengambil input dari pengguna dan parsing menggunakan ast.literal_eval untuk keamanan
#             matrix = req.POST.get('matrix')  # Input matriks dalam bentuk string
#             results = req.POST.get('results')  # Input hasil dalam bentuk string

#             # Menggunakan ast.literal_eval untuk parsing input secara aman
#             matrix = ast.literal_eval(matrix)  # Menghindari penggunaan eval() yang tidak aman
#             results = ast.literal_eval(results)

#             # Jalankan metode eliminasi Gauss
#             steps, descriptions, result, back_sub_steps = eliminasi_gauss(matrix, results)
#             combined_steps = list(zip(steps, descriptions))

#             # Membuat grafik menggunakan Plotly jika terdapat langkah eliminasi
#             if steps:
#                 traces = []
#                 for step_idx, step in enumerate(steps):
#                     # Membuat heatmap dari setiap langkah eliminasi
#                     trace = go.Heatmap(z=step, coloraxis="coloraxis", name=f'Step {step_idx + 1}')
#                     traces.append(trace)

#                 layout = go.Layout(
#                     title='Proses Eliminasi Gauss',
#                     xaxis=dict(title='Kolom'),
#                     yaxis=dict(title='Baris'),
#                     template='plotly_white',
#                     coloraxis=dict(colorscale='Viridis')
#                 )

#                 fig = go.Figure(data=traces, layout=layout)
#                 plot_div = pio.to_html(fig, full_html=False)

#         except ValueError:
#             error_message = "Masukkan nilai numerik yang valid."
#         except (SyntaxError, NameError):
#             error_message = "Masukkan input matriks dan hasil yang valid."

#     return render(req, 'gaus/pages/index.html', {
#         'result': result,
#         'steps': steps,
#         'descriptions': descriptions,
#         'error_message': error_message,
#         'plot_div': plot_div,
#         'matrix': req.POST.get('matrix'),
#         'results': req.POST.get('results'),
#         'combined_steps': combined_steps,
#         'back_sub_steps': back_sub_steps,
#     })







# # from django.shortcuts import render
# # import plotly.graph_objs as go
# # import plotly.io as pio
# # import numpy as np
# # import ast  # Digunakan untuk parsing input yang aman

# # # Fungsi Metode Eliminasi Gauss
# # def eliminasi_gauss(matrix, results):
# #     # Mengubah matriks input dan hasil menjadi matriks augmented
# #     augmented_matrix = np.array(matrix, dtype=float)
# #     results_vector = np.array(results, dtype=float).reshape(-1, 1)
# #     augmented_matrix = np.hstack((augmented_matrix, results_vector))
# #     n = len(results)

# #     steps = []  # Untuk menyimpan langkah-langkah eliminasi
# #     descriptions = []  # Untuk menyimpan deskripsi langkah

# #     # Forward Elimination
# #     for i in range(n):
# #         # Pivoting jika elemen diagonal utama adalah nol
# #         if augmented_matrix[i, i] == 0:
# #             for k in range(i + 1, n):
# #                 if augmented_matrix[k, i] != 0:
# #                     augmented_matrix[[i, k]] = augmented_matrix[[k, i]]
# #                     descriptions.append(f"Menukar baris {i + 1} dengan baris {k + 1} karena elemen pivot bernilai nol.")
# #                     break
# #             else:
# #                 return None, "Tidak ada solusi unik."
        
# #         # Normalisasi baris pivot
# #         pivot_value = augmented_matrix[i, i]
# #         augmented_matrix[i] = augmented_matrix[i] / pivot_value
# #         descriptions.append(f"Normalisasi baris {i + 1} dengan membagi semua elemen dengan {int(pivot_value) if pivot_value.is_integer() else pivot_value}.")
# #         steps.append(augmented_matrix.copy())

# #         # Eliminasi untuk membuat nol di bawah elemen pivot
# #         for j in range(i + 1, n):
# #             factor = augmented_matrix[j, i]
# #             augmented_matrix[j] = augmented_matrix[j] - factor * augmented_matrix[i]
# #             descriptions.append(f"Mengurangi baris {j + 1} dengan baris {i + 1} dikalikan {int(factor) if factor.is_integer() else factor} untuk membuat elemen di bawah pivot menjadi nol.")
# #             steps.append(augmented_matrix.copy())

# #     # Back Substitution
# #     x = np.zeros(n)
# #     for i in range(n - 1, -1, -1):
# #         x[i] = augmented_matrix[i, -1] - np.sum(augmented_matrix[i, i + 1:n] * x[i + 1:n])
# #         descriptions.append(f"Melakukan substitusi balik untuk menghitung nilai x{i + 1}.")

# #     # Mengganti nilai -0.0 dengan 0.0 untuk kejelasan di augmented matrix dan hasil
# #     augmented_matrix[augmented_matrix == -0.0] = 0.0
# #     x[x == -0.0] = 0.0

# #     return steps, descriptions, x


# # def index(req):
# #     """
# #     Fungsi view untuk menangani permintaan halaman utama dan menghitung sistem persamaan linear menggunakan metode eliminasi Gauss.
    
# #     Mengambil input dari pengguna, menjalankan metode eliminasi Gauss, dan mengembalikan hasil serta langkah-langkah perhitungan.
# #     """
# #     result = None
# #     error_message = None
# #     steps = []
# #     descriptions = []
# #     plot_div = None

# #     if req.method == 'POST':
# #         try:
# #             # Mengambil input dari pengguna dan parsing menggunakan ast.literal_eval untuk keamanan
# #             matrix = req.POST.get('matrix')  # Input matriks dalam bentuk string
# #             results = req.POST.get('results')  # Input hasil dalam bentuk string

# #             # Menggunakan ast.literal_eval untuk parsing input secara aman
# #             matrix = ast.literal_eval(matrix)  # Menghindari penggunaan eval() yang tidak aman
# #             results = ast.literal_eval(results)

# #             # Jalankan metode eliminasi Gauss
# #             steps, descriptions, result = eliminasi_gauss(matrix, results)
# #             combined_steps = list(zip(steps, descriptions))

# #             # Membuat grafik menggunakan Plotly jika terdapat langkah eliminasi
# #             if steps:
# #                 traces = []
# #                 for step_idx, step in enumerate(steps):
# #                     # Membuat heatmap dari setiap langkah eliminasi
# #                     trace = go.Heatmap(z=step, coloraxis="coloraxis", name=f'Step {step_idx + 1}')
# #                     traces.append(trace)

# #                 layout = go.Layout(
# #                     title='Proses Eliminasi Gauss',
# #                     xaxis=dict(title='Kolom'),
# #                     yaxis=dict(title='Baris'),
# #                     template='plotly_white',
# #                     coloraxis=dict(colorscale='Viridis')
# #                 )

# #                 fig = go.Figure(data=traces, layout=layout)
# #                 plot_div = pio.to_html(fig, full_html=False)

# #         except ValueError:
# #             error_message = "Masukkan nilai numerik yang valid."
# #         except (SyntaxError, NameError):
# #             error_message = "Masukkan input matriks dan hasil yang valid."

# #     return render(req, 'gaus/pages/index.html', {
# #         'result': result,
# #         'steps': steps,
# #         'descriptions': descriptions,
# #         'error_message': error_message,
# #         'plot_div': plot_div,
# #         'matrix': req.POST.get('matrix'),
# #         'results': req.POST.get('results'),
# #         'combined_steps': combined_steps,
# #     })
