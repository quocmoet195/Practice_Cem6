import matplotlib.pyplot as plt

def plot_results(results, max_errors):
    """Строит и отображает график распространения ошибок для различных режимов AES"""
    plt.figure(figsize=(10, 8))
    
    for mode_name, data_points in results.items():
        n_values = [p[0] for p in data_points]
        m_values = [p[1] for p in data_points]
        plt.plot(n_values, m_values, marker='o', linestyle='-', label=mode_name)
        
    x_theory = list(range(1, max_errors + 1))
    y_theory_1 = x_theory
    y_theory_2 = [2 * x for x in x_theory]
    
    plt.plot(x_theory, y_theory_1, 'k--', label='Теория  M=N (ECB, OFB)')
    plt.plot(x_theory, y_theory_2, 'k:', label='Теория  M=2N (CBC, CFB)')

    plt.title('Распространение ошибок в режимах AES')
    plt.xlabel('Число повреждённых блоков шифртекста (N)')
    plt.ylabel('Число повреждённых блоков открытого текста (M)')
    plt.xticks(range(1, max_errors + 1))
    plt.yticks(range(0, (max_errors * 2) + 2, 2))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    output_filename = "error_propagation_graph.png"
    plt.savefig(output_filename)
    print(f"\nЭксперимент завершен. График сохранен как {output_filename}")
    plt.show()