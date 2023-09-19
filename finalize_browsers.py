import psutil

def close_all_browsers():
    # Nome do processo do Chrome
    chrome_process_name = "chrome.exe"

    # Obtém a lista de todos os processos em execução
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.name() == chrome_process_name:
            try:
                # Encerra o processo do Chrome
                process_obj = psutil.Process(process.pid)
                process_obj.terminate()
            except Exception as e:
                print(f"Erro ao encerrar o processo: {e}")

    # print("Todos os processos do Google Chrome foram encerrados.")
