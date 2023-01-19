# suxess-why-why-why

## Warum container

### All-in-one-Packages inkl. aller notwendigen Dependencies erstellen, veroeffentlichen und wiederverwenden

Ausgangslage:

Wir haben eine Python-Webapplikation geschrieben, die wir gerne vertreiben wollen.

Dieses Python-Projekt direkt am Rechner ausführen führt möglicherweise zu folgendem Problem:

    python3 app.py
    Traceback (most recent call last):
    File "app.py", line 1, in <module>
        from flask import Flask, render_template, request, session, redirect, url_for
    ModuleNotFoundError: No module named 'flask'

Im `Dockerfile` wird beschrieben, was alles im Container enthalten sein soll und welches Programm er ausführen soll.

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


### Third-Party Software verwenden

Wordpress (ohne Datenbank)

    docker run -p 8080:80 wordpress

Wordpress (inkl. Datenbank-Container)

    # startet zwei container 
    docker-compose -f stack.yml up