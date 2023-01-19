# -*- coding: utf-8 -*-


def formatPages(pageToTemplate = "https://openiti.org/about.html", baseUrl = "https://openiti.org", staticTemplate = None):
    import os
    import re
    import urllib.request
    
    currentDir = os.getcwd()
    dataDir = os.path.join(currentDir, "authors")
    print(dataDir)
    
    # Create a dictionary where keys are the parent dir for the book and values are a list of links
    # NOTE - THIS IS NOT ABLE TO HANDLE BOOK FOLDERS (I.E. 2 LEVELS OF DEPTH) - NEED TO MODIFY IF DIR STRUCTURE CHANGES
    dirDict = {}
    for folder in os.listdir(dataDir):
        print(folder)
        path = os.path.join(dataDir, folder)
        if os.path.isdir(path):
            fileList = []
            for file in os.listdir(path):
                if re.search(r".*\.html", file):                    
                    fileList.append(file)
            dirDict[folder] = fileList
    print(dirDict)

    # Fetch the webpage html to template
    if staticTemplate:
        with open(staticTemplate, "r") as f:
            pageHtml = f.read()
            f.close()
    else:
        fp = urllib.request.urlopen(pageToTemplate)
        mybytes = fp.read()
        pageHtml = mybytes.decode("utf8")
        fp.close()
    
    # Clean up links to fetch the correct assets from the baseURL
    
    assetPath = 'href= "{}/assets'.format(baseUrl)
    pageHtml = re.sub(r'href\s?=\s?"/assets', assetPath, pageHtml)
    
    assetPath = 'src= "{}/assets'.format(baseUrl)
    pageHtml = re.sub(r'src\s?=\s?"/assets', assetPath, pageHtml)
    
    # Split text on <main> and </main> to get page template to wrap around new elements
    preMainHtml = re.split(r"<main", pageHtml)[0]
    postMainHtml = re.split(r"</main>", pageHtml)[-1]
    
    
    # Loop through to create an index of author URIs linking to index pages for authors
    # For each author page create index of document pages
    # For every page, wrap in the existing html, and for document pages ensure the doc-specific stylesheet is used
    authorIndexTitle = '''<header class="section-title">
                          <h2>Digital Publications</h2>
                          </header>'''
    authorIndex = [preMainHtml, '<main class="page-content" aria-label="Content">', '<div class="index inner">', authorIndexTitle]
    for author in dirDict.keys():
        documentIndexTitle = '''<header class="section-title">
                          <h2>
                          <a href="javascript:history.go(-1)">Digital Publications</a>
                          <span class="icon icon--arrow-right">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
                        <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
                        </svg></span>
                          {}</h2>
                          </header>'''.format(author)
        documentIndex = [preMainHtml, '<main class="page-content" aria-label="Content">', '<div class="index inner">', documentIndexTitle]
        authorPage = './authors/{}.html'.format(author)
        authorLinkHtml = '''<h3 class="entry-title">
            <a href="{}" class="more-link">{}<span class="icon icon--arrow-right">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
            <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
            </svg></span></a></h3>'''.format(authorPage,author)
        authorIndex.append(authorLinkHtml)
        for document in dirDict[author]:
            documentPage = "./{}/{}".format(author, document)
            print(documentPage)
            documentLinkHtml = '''<h3 class="entry-title">
            <a href="{}" class="more-link">{}<span class="icon icon--arrow-right">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
            <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
            </svg></span></a></h3>'''.format(documentPage, document.split(".html")[0])
            documentIndex.append(documentLinkHtml)
            ## NEED TO WRAP DOCUMENT PAGE HERE AND OUTPUT
            documentTitle = '''<header class="section-title">
                          <h2>
                          <a href="javascript:history.go(-1)">{}</a>
                          <span class="icon icon--arrow-right">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
                        <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
                        </svg></span>
                          {}</h2>
                          </header>'''.format(author, ".".join(document.split(".")[1:3]))
            
            documentPath = os.path.join(dataDir, "{}/{}".format(author, document))
            with open(documentPath, "r", encoding='utf-8-sig') as f:                
                textContent = f.read()
                f.close()
            stylesheetIn = re.findall(r'<link rel="stylesheet"[^>]+>', textContent)
            stylesheetTemp = re.findall(r'<link rel="stylesheet"[^>]+>', preMainHtml)
            
            
            textContent = "\n".join(re.split(r"(</?body>)", textContent)[1:4])
            print(textContent)
            
            preMainHtmlSplit = re.split(r'(<link rel="stylesheet"[^>]+>)', preMainHtml)
            
            print(preMainHtmlSplit[1])
            for sheet in stylesheetIn:
                if sheet not in stylesheetTemp:
                    print(sheet)
                    preMainHtmlSplit.insert(2, sheet)
            preMainHtmlForDoc = "\n".join(preMainHtmlSplit)
            fullHtml = "\n".join([preMainHtmlForDoc, '<main class="page-content" aria-label="Content">', '<div class="index inner">', documentTitle, textContent, postMainHtml])
            
            with open(documentPath, "w", encoding = "utf-8-sig") as f:
                f.write(fullHtml)
                f.close()
        documentIndex.extend(['</div>', '</main>', postMainHtml])
        documentIndexHtml = "\n".join(documentIndex)
        with open(authorPage, "w") as f:
            f.write(documentIndexHtml)
            f.close()
    authorIndex.extend(['</div>', '</main>', postMainHtml])
    authorIndexHtml = "\n".join(authorIndex)
    with open("index.html", "w") as f:
        f.write(authorIndexHtml)
        f.close()
    
            
        
        