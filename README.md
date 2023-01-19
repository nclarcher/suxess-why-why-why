# suxess-why-why-why

## Warum Container

Ausgangslage:

Wir (oder ChatGPT) haben eine Python-Webapplikation geschrieben, die wir gerne vertreiben wollen.

Dieses Python-Projekt direkt am Rechner ausführen, führt möglicherweise zu folgendem Problem:

    python3 app.py
    Traceback (most recent call last):
    File "app.py", line 1, in <module>
        from flask import Flask, render_template, request, session, redirect, url_for
    ModuleNotFoundError: No module named 'flask'

Das zeigt schon eines der Probleme mit traditionellen Applikationen:
    - das Management aller Dependencies um die Applikation herum
    - wie die Software gestartet / gestoppt / gemanaged wird ist je nach Software unterschiedlich

Lösung: Im `Dockerfile` wird beschrieben, was alles für die Applikation benötigt wird und wie die Software gestartet werden muss.
Das Bauen, Bereitstellen und Starten/Stoppen ist dann für jeden Container gleich, ganz unabhängig welche Software sich im Container befindet.

Container Image bauen

    docker build -t why-container .

Container starten

    docker run -p 80:5000 why-container

Container Image publishen in öffentliche Registry

    export CR_PAT=<your-github-personal-access-token>
    echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
    > Login Succeeded
    docker tag why-container ghcr.io/jkleinlercher/why-container
    docker push ghcr.io/jkleinlercher/why-container:latest

Image ist jetzt auf https://github.com/jkleinlercher/suxess-why-why-why/pkgs/container/why-container verfügbar  

Container Image von github registry ziehen und laufen lassen

    docker run -d -p 80:5000 ghcr.io/jkleinlercher/why-container

Auf Webapplikation zugreifen

    curl -L http://localhost

Zusatzcommands

    # multiple arch build and push
    docker buildx create --name mybuilder
    docker buildx use mybuilder
    docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v8 -t ghcr.io/jkleinlercher/why-container:latest . --push

### Mehrere Instanzen starten

    docker run -d --name webserver-1 -p 81:5000 ghcr.io/jkleinlercher/why-container
    docker run -d --name webserver-2 -p 82:5000 ghcr.io/jkleinlercher/why-container
    docker run -d --name webserver-3 -p 83:5000 ghcr.io/jkleinlercher/why-container

### Third-Party Software verwenden

Wordpress (ohne Datenbank)

    docker run -p 8080:80 wordpress

Wordpress (inkl. Datenbank-Container)

    # startet zwei container 
    docker-compose -f stack.yml up


## Warum Kubernetes

### Container im Cluster starten, ohne zu sagen wo sie gestartet werden sollen

Den obigen Container in einem K8s Cluster starten

    kubectl run why-kubernetes --name=ghcr.io/jkleinlercher/why-container

Wichtig: obwohl der Cluster aus mehreren Nodes besteht, müssen wir nicht sagen wo der Container gestartet wird. Darum kümmert sich K8s.

### Einfaches skalieren

Gleich 10 Instanzen meiner Applikation starten (siehe replicas Attribut im deployment)

    kubectl apply -f kubernetes/deployment.yaml

Down-Scale auf 2 Deployments (imperativ)

    kubectl scale deployment why-kubernetes --replicas=2

Up-Scale auf 3 Deployments (deklarativ)

    # Anpassen des deployment.yaml
    kubectl apply -f kubernetes/deployment.yaml

### Applikation von außen erreichbar machen und Requests auf alle Instanzen verteilen

Applikation von außen erreichbar machen über Ingress (so etwas wie ein Reverse-Proxy)

    kubectl expose deployment why-kubernetes --type=ClusterIP --target-port=5000 --port=80
    kubectl apply -f kubernetes/ingress.yaml
    curl http://localhost:8081/

### Kubernetes ist ein selbstheilendes System

    watch kubectl get pods
    kubectl delete pod <eine-instanz-auswaehlen>
