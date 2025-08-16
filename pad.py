from codigo import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) 
    
# funcionalidades de execução de tarefas em paralelo ou chamadas a própria
# api podem quebrar quando rodamos o app em debug