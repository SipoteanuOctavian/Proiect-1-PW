import socket
import os
import threading
import gzip
from io import BytesIO

def get_content_type(file_path):
    """Return the content type based on the file extension."""
    if file_path.endswith('.html'):
        return 'text/html'
    elif file_path.endswith('.css'):
        return 'text/css'
    elif file_path.endswith('.js'):
        return 'application/js'
    elif file_path.endswith('.png'):
        return 'text/png'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return 'text/jpeg'
    elif file_path.endswith('.gif'):
        return 'text/gif'
    elif file_path.endswith('.ico'):
        return 'image/x-icon'
    else:
        return 'application/octet-stream'

def compress_content(content):
    """Compress content using gzip."""
    buf = BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='w') as f:
        f.write(content)
    return buf.getvalue()

def handle_request(client_socket, address):
    """Handle client request."""
    print(f"S-a conectat un client de la adresa: {address}")

    # Citirea cererii HTTP
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Cerere:\n{request_data}")

    # Extrage path-ul resursei cerute
    request_lines = request_data.split('\n')
    first_line = request_lines[0]
    url = first_line.split(' ')[1]

    # Construiește calea locală a resursei
    file_path = 'continut' + url

    # Verifică dacă fișierul există
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            file_content = file.read()
        
        # Comprimă conținutul
        compressed_content = compress_content(file_content)
        
        # Construiește răspunsul HTTP
        content_type = get_content_type(file_path)
        response_header = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\nContent-Length: {str(len(compressed_content))}\nContent-Encoding: gzip\n\n"
        response_data = response_header.encode('utf-8') + compressed_content

    else:
        response_data = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<h1>404 Not Found</h1>".encode('utf-8')

    # Trimite răspunsul către client
    client_socket.sendall(response_data)

    # Închide conexiunea
    client_socket.close()

def main():
    """Main function to start the server."""
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', 5678))
    serversocket.listen(5)
    print("Serverul asculta cereri la adresa http://localhost:5678/")

    client_threads = []

    try:
        while True:
            print('#########################################################################')
            print('Serverul ascultă potențiali clienți.')
            
            # Așteaptă conectarea unui client la server
            # Metoda `accept` este blocantă => clientsocket, care reprezintă socket-ul corespunzător clientului conectat
            (clientsocket, address) = serversocket.accept()
            
            # Crearea unui fir de execuție pentru a gestiona clientul
            client_handler = threading.Thread(target=handle_request, args=(clientsocket, address))
            client_handler.start()
            client_threads.append(client_handler)

            print('S-a terminat comunicarea cu clientul.')
    except KeyboardInterrupt:
        print("Serverul a fost oprit.")
        # Închide toate thread-urile active
        for thread in client_threads:
            thread.join()

    finally:
        serversocket.close()

if __name__ == "__main__":
    main()
