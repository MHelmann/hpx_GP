import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def visual_matrix(n_tiles):
    tiled_cholesky_seq = []
    C = np.zeros((n_tiles * n_tiles, ), dtype=object)
    # 0 Iteration
    #print(C.reshape((n_tiles, n_tiles)))
    #tiled_cholesky_seq.append(C.reshape((n_tiles, n_tiles)).copy())
    # Tiled Cholesky decomposition
    for k in range(0, n_tiles):
        # POTRF
        C[k *n_tiles + k] = 'p'
        # print(C.reshape((n_tiles, n_tiles)))
        tiled_cholesky_seq.append(C.reshape((n_tiles, n_tiles)).copy())
        for m in range(k+1,n_tiles):
            # TRSM
            C[m *n_tiles + k] = 'm'
            # print(C.reshape((n_tiles, n_tiles)))
            tiled_cholesky_seq.append(C.reshape((n_tiles, n_tiles)).copy())
        for m in range(k+1,n_tiles):
            # SYRK
            C[m *n_tiles + m] = 's'
            # print(C.reshape((n_tiles, n_tiles)))
            tiled_cholesky_seq.append(C.reshape((n_tiles, n_tiles)).copy())
            for n in range(k+1,m):
                # GEMM
                C[m *n_tiles + n] = 'g'
                # print(C.reshape((n_tiles, n_tiles)))
                tiled_cholesky_seq.append(C.reshape((n_tiles, n_tiles)).copy())
        
    return tiled_cholesky_seq


def plot_tiled_cholesky(tiled_cholesky_seq):

    matrices = tiled_cholesky_seq
    str_to_int = {0: 0, 'p': 1, 'm': 2, 's': 3, 'g': 4}
    int_to_str = {0: 0, 1: 'p', 2: 'm', 3: 's', 4: 'g'}

    matrices_numeric = []
    for matrix in matrices:
        matrix_numeric = np.zeros_like(matrix, dtype=int)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                matrix_numeric[i, j] = str_to_int[matrix[i, j]]
        matrices_numeric.append(matrix_numeric)

    # define color map 
    color_map = {0: np.array([0, 0, 0]),   # Black
                 1: np.array([255, 0, 0]), # Red
                 2: np.array([0, 255, 0]), # Green
                 3: np.array([255, 255, 0]), # Yellow
                 4: np.array([0, 0, 255])} # Blue

    # Determine the number of rows and columns for subplots
    num_matrices = len(matrices)
    num_rows = (num_matrices + 3) // 4  # Round up to the nearest multiple of 4
    num_cols = min(num_matrices, 4)

    # Plot each matrix
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(16, 4*num_rows))  # Adjust the figure width here

    for m, ax in enumerate(axes.flat):
        if m < num_matrices:
            # make a 3d numpy array that has a color channel dimension   
            data_3d = np.ndarray(shape=(matrices_numeric[m].shape[0], matrices_numeric[m].shape[1], 3), dtype=int)
            for i in range(0, matrices_numeric[m].shape[0]):
                for j in range(0, matrices_numeric[m].shape[1]):
                    data_3d[i][j] = color_map[matrices_numeric[m][i][j]]
            
            # display the plot 
            ax.imshow(data_3d)
            ax.axis('off')

            for i in range(0, matrices_numeric[m].shape[0]):
                for j in range(0, matrices_numeric[m].shape[1]):
                    c = matrices_numeric[m][j,i]
                    ax.text(i, j, str(int_to_str[c]), va='center', ha='center')


    legend_labels = ['Untouched', 'POTRF', 'TRSM', 'SYRK', 'GEMM']  # Custom labels
    legend_handles = [mpatches.Patch(color=color_map[key] / 255.0, label=label) for key, label in zip(int_to_str, legend_labels)]  # Customize labels
    fig.legend(handles=legend_handles, loc='lower center', ncol=len(legend_labels), bbox_to_anchor=(0.5, 0.05))


    plt.show()


if __name__ == '__main__':

    n_tiles = 4
    tiled_cholesky_seq = visual_matrix(n_tiles)
    plot_tiled_cholesky(tiled_cholesky_seq)