# -*- coding: utf-8 -*-


def formatPages(pageToTemplate = "https://openiti.org/about.html", baseUrl = "https://openiti.org", publicationsBaseUrl = "https://mabarber92.github.io/digital-publications", staticTemplate = None):
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
                regex = folder + ".*\.html"
                if re.search(regex, file):                    
                    fileList.append(file)
            fileList = sorted(fileList)
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
    
    # Split text on <main> and </main> or <div class="inner">[^>]+<div class="intro-text"> to get page template to wrap around new elements
    if len(re.findall('<div class="inner">[^>]+<div class="intro-text">', pageHtml)) > 0:
        preMainHtml = re.split('<div class="inner">[^>]+<div class="intro-text">', pageHtml)[0]
    else:
        preMainHtml = re.split(r"<main", pageHtml)[0]
    postMainHtml = re.split(r"</main>", pageHtml)[-1]
    
    # Clean up jekyll meta that's not useful
    metaCleanRegex = r'<meta property="og:url[^>]+>|<link rel="canonical"[^>]+>|<script type="application/ld\+json">[^>]+>'
    preMainHtml = re.sub(metaCleanRegex, "", preMainHtml)
    
    # Fetch parts of metadata to customise on pages
    htmlTitle = re.findall(r'<title>[^>]+>', preMainHtml)
    if len(htmlTitle) > 0:
        htmlTitle = htmlTitle[0]
    else:
        htmlTitle = None
    metaTitle = re.findall(r'<meta property="og:title"[^>]+>', preMainHtml)
    if len(metaTitle) > 0:
        metaTitle = metaTitle[0]
    else:
        metaTitle = None
    twitterTitle = re.findall(r'<meta property="twitter:title"[^>]+>', preMainHtml)
    if len(twitterTitle) > 0:        
        twitterTitle = twitterTitle[0]
    else:
        twitterTitle = None
    
    print([htmlTitle, metaTitle, twitterTitle])
    # Loop through to create an index of author URIs linking to index pages for authors
    # For each author page create index of document pages
    # For every page, wrap in the existing html, and for document pages ensure the doc-specific stylesheet is used
    authorIndexTitle = '''<header class="section-title">
                          <h2>Digital Publications</h2>
                          </header>'''
    
    # Edit page metadata to reflex page
    preMainHtmlAuthorIndex = preMainHtml[:]
    if htmlTitle:
        newTitle = '<title>Digital Publications | Open Islamicate Texts Initiative</title>'        
        preMainHtmlAuthorIndex = re.sub(htmlTitle, newTitle, preMainHtmlAuthorIndex)
    if metaTitle:
        newTitle = '<meta property="og:title" content="Digital Publications" />'      
        preMainHtmlAuthorIndex = re.sub(metaTitle, newTitle, preMainHtmlAuthorIndex)
    if twitterTitle:
        newTitle = '<meta property="twitter:title" content="Digital Publications" />'        
        preMainHtmlAuthorIndex = re.sub(twitterTitle, newTitle, preMainHtmlAuthorIndex)
    authorIndex = [preMainHtmlAuthorIndex, '<main class="page-content" aria-label="Content">', '<div class="index inner">', authorIndexTitle]
    for author in dirDict.keys():
        documentIndexTitle = '''<header class="section-title">
                          <h2>
                          <a href={}>Digital Publications</a>
                          <span class="icon icon--arrow-right">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
                        <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
                        </svg></span>
                          {}</h2>
                          </header>'''.format(publicationsBaseUrl, author)
        # Edit page metadata to reflex page
        preMainHtmlDocumentIndex = preMainHtml[:]
        if htmlTitle:
            newTitle = '<title>{} | Open Islamicate Texts Initiative</title>'.format(author)        
            preMainHtmlDocumentIndex = re.sub(htmlTitle, newTitle, preMainHtmlDocumentIndex)
        if metaTitle:
            newTitle = '<meta property="og:title" content="{}" />'.format(author)      
            preMainHtmlDocumentIndex = re.sub(metaTitle, newTitle, preMainHtmlDocumentIndex)
        if twitterTitle:
            newTitle = '<meta property="twitter:title" content="{}" />'.format(author)        
            preMainHtmlDocumentIndex = re.sub(twitterTitle, newTitle, preMainHtmlDocumentIndex)
        
        documentIndex = [preMainHtmlDocumentIndex, '<main class="page-content" aria-label="Content">', '<div class="index inner">', documentIndexTitle]
        authorPage = './authors/{}/index.html'.format(author)
        authorLink = '{}/authors/{}'.format(publicationsBaseUrl, author)
        authorLinkHtml = '''<h3 class="entry-title">
            <a href="{}" class="more-link">{}<span class="icon icon--arrow-right">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
            <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
            </svg></span></a></h3>'''.format(authorLink,author)
        authorIndex.append(authorLinkHtml)
        for document in dirDict[author]:
            documentName = ".".join(document.split(".")[1:3])
            documentPage = "./{}".format(document)
            
            documentLinkHtml = '''<h3 class="entry-title">
            <a href="{}" class="more-link">{}<span class="icon icon--arrow-right">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
            <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
            </svg></span></a></h3>'''.format(documentPage, document.split(".html")[0])
            documentIndex.append(documentLinkHtml)
            ## NEED TO WRAP DOCUMENT PAGE HERE AND OUTPUT
            documentTitle = '''<header class="section-title">
                          <h2>
                          <a href="{}">{}</a>
                          <span class="icon icon--arrow-right">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="50.4 -114.8 16 16">
                        <path d="M63.1-107.7l-6.7-6.7c-.2-.3-.6-.4-.9-.4-.4 0-.7.1-.9.4l-.8.8c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l5 5-5 5c-.3.3-.4.6-.4.9 0 .4.1.7.4.9l.8.8c.3.3.6.4.9.4.4 0 .7-.1.9-.4l6.7-6.7c.3-.3.4-.6.4-.9 0-.4-.2-.7-.4-.9z"/>
                        </svg></span>
                          {}</h2>
                          </header>'''.format(authorLink, author, documentName)
            
            documentPath = os.path.join(dataDir, "{}/{}".format(author, document))
            with open(documentPath, "r", encoding='utf-8-sig') as f:                
                textContent = f.read()
                f.close()
            stylesheetIn = re.findall(r'<link rel="stylesheet"[^>]+>', textContent)
            stylesheetTemp = re.findall(r'<link rel="stylesheet"[^>]+>', preMainHtml)
            
            
            textContent = "\n".join(re.split(r"(</?body>)", textContent)[1:4])
            
            
            preMainHtmlSplit = re.split(r'(<link rel="stylesheet"[^>]+>)', preMainHtml)
            
            print(preMainHtmlSplit[1])
            for sheet in stylesheetIn:
                if sheet not in stylesheetTemp:
                    
                    preMainHtmlSplit.insert(2, sheet)
            preMainHtmlForDoc = "\n".join(preMainHtmlSplit)
            
            # Edit page metadata to reflex page
           
            if htmlTitle:
                newTitle = '<title>{}| Open Islamicate Texts Initiative</title>'.format(documentName)        
                preMainHtmlForDoc = re.sub(htmlTitle, newTitle, preMainHtmlForDoc)
            if metaTitle:
                newTitle = '<meta property="og:title" content="{}" />'.format(documentName)      
                preMainHtmlForDoc = re.sub(metaTitle, newTitle, preMainHtmlForDoc)
            if twitterTitle:
                newTitle = '<meta property="twitter:title" content="{}" />'.format(documentName)        
                preMainHtmlForDoc = re.sub(twitterTitle, newTitle, preMainHtmlForDoc)
            
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

if __name__ == '__main__':
    formatPages()
            
        
        
