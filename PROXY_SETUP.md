# Proxy Configuration Instructions

**IF YOU WANT TO USE A PROXY, THEN YOU MUST CREATE A FILE `proxies.txt` AND SPECIFY EACH PROXY SERVER ON A NEW LINE. THIS IS NOT NECESSARY. SOCKS ARE SUPPORTED.**

**TEMPLATE FOR SPECIFYING PROXY SERVERS:**
<protocol>://[<USERNAME>:<PASSWORD>@]<HOST>[:<PORT>]

**SUPPORTED PROTOCOLS:** HTTP, HTTPS, SOCKS4, SOCKS5

---

### Examples of Proxy Configurations

Here are some examples of how to specify proxy servers:

- **HTTP Proxy with Domain Name:**
  ```
  http://user:password@proxy.example.com:8080
  ```

- **HTTPS Proxy with Domain Name:**
  ```
  https://user:password@secureproxy.example.com:443
  ```

- **SOCKS4 Proxy with Domain Name:**
  ```
  socks4://proxy.example.com:1080
  ```

- **SOCKS5 Proxy with Domain Name:**
  ```
  socks5://proxy.example.com:1080
  ```

- **HTTP Proxy with IP Address:**
  ```
  http://user:password@192.168.1.1:8080
  ```

- **HTTPS Proxy with IP Address:**
  ```
  https://user:password@192.168.1.2:443
  ```

- **SOCKS4 Proxy with IP Address:**
  ```
  socks4://192.168.1.3:1080
  ```

- **SOCKS5 Proxy with IP Address:**
  ```
  socks5://192.168.1.4:1080
  ```

### Explanation of Each Field

- `<USERNAME>` and `<PASSWORD>` - Only required if your proxy requires authentication.
- `<HOST>` - The address of the proxy server, which can be either a domain name or an IP address.
- `<PORT>` - The port on which the proxy server is running.

### Troubleshooting Tips

If you cannot connect to the internet, check the following:

- Ensure that the port and address are correct.
- Make sure that your proxy server is operational and accessible.
- Do not use free proxy servers to transfer confidential information. Such servers are also unstable and may not work
- If your https proxy is not working, try changing the protocol to http://
