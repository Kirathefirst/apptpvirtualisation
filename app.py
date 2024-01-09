import os
import docker
from flask import Flask, request, render_template

app = Flask(__name__)


DOCKER_HUB_USERNAME = 'kirathefirst'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        
        
        filename = f.filename
        filepath = os.path.join(os.getcwd(), filename)
        f.save(filepath)
        
        try:
            
            client = docker.from_env()
            image, _ = client.images.build(path=os.getcwd(), dockerfile="Dockerfile")
            
            # Tag et poussez l'image vers Docker Hub
            docker_hub_repo = f"{DOCKER_HUB_USERNAME}/{filename}"
            image.tag(docker_hub_repo, "latest")
            client.images.push(docker_hub_repo)
            
            # Supprimer le fichier après utilisation
            os.remove(filepath)
            
            return 'Fichier téléchargé et poussé sur Docker Hub avec succès!'
        
        except Exception as e:
            # Gestion des erreurs
            return f"Erreur lors de la création ou de la poussée de l'image : {e}"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
