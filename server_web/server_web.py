import socket
import os
import threading
import gzip
from io import BytesIO

# Define the path to the 'continut' directory
CONTENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'continut')

def get_content_type(file_path):
    """Return the content type based on the file extension."""
    if file_path.endswith('.html'):
        return 'text/html'
    elif file_path.endswith('.css'):
        return 'text/css'
    elif file_path.endswith('.js'):
        return 'application/javascript'
    elif file_path.endswith('.png'):
        return 'image/png'
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return 'image/jpeg'
    elif file_path.endswith('.gif'):
        return 'image/gif'
    elif file_path.endswith('.ico'):
        return 'image/x-icon'
    else:
        return 'application/octet-stream'

def compress_content(content):
    """Compress content using gzip."""
    buf = BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(content)
    return buf.getvalue()

def handle_request(client_socket, address):
    """Handle client request."""
    print(f"S-a conectat un client de la adresa: {address}")

    try:
        # Citirea cererii HTTP
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"Cerere:\n{request_data}")

        # Verifică dacă cererea HTTP este validă
        request_lines = request_data.split('\n')
        if len(request_lines) == 0 or len(request_lines[0].split(' ')) < 2:
            raise ValueError("Invalid HTTP request")

        first_line = request_lines[0]
        url = first_line.split(' ')[1]
        
        # Logging the requested URL
        print(f"Requested URL: {url}")

        # Construiește calea locală a resursei
        file_path = os.path.join(CONTENT_DIR, url.lstrip('/'))
        if url == '/':
            file_path = os.path.join(CONTENT_DIR, 'index.html')  # Default to index.html if root is requested
        
        # Logging the constructed file path
        print(f"File path: {file_path}")

        # Verifică dacă fișierul există
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            # Comprimă conținutul
            compressed_content = compress_content(file_content)
            
            # Construiește răspunsul HTTP
            content_type = get_content_type(file_path)
            response_header = (f"HTTP/1.1 200 OK\r\n"
                               f"Content-Type: {content_type}\r\n"
                               f"Content-Length: {str(len(compressed_content))}\r\n"
                               f"Content-Encoding: gzip\r\n\r\n")
            response_data = response_header.encode('utf-8') + compressed_content

        else:
            # Logging file not found
            print(f"File not found: {file_path}")
            response_data = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>".encode('utf-8')

        # Trimite răspunsul către client
        client_socket.sendall(response_data)

    except ValueError as e:
        print(f"Error: {e}")
        response_data = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<h1>400 Bad Request</h1>".encode('utf-8')
        client_socket.sendall(response_data)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        response_data = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n<h1>500 Internal Server Error</h1>".encode('utf-8')
        client_socket.sendall(response_data)

    finally:
        # Închide conexiunea
        client_socket.close()

def main():
    """Main function to start the server."""
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', 5679))  # Changed port to 5679
    serversocket.listen(5)
    print("Serverul asculta cereri la adresa http://localhost:5679/")

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

