from checker import (build_url, is_https, show_response, check_site,
                     scan_sites, check_headers, retry_check)

# Partea 1: apeluri pentru build_url și is_https
print("Partea 1, build_url fără /:", build_url("example.com", "login"))
print("Partea 1, build_url cu /:", build_url("example.com", "/login"))
print("Partea 1, is_https cu https:", is_https("https://example.com"))
print("Partea 1, is_https cu http:", is_https("http://example.com"))

# Partea 2: apeluri pentru show_response
print("Partea 2, show_response pe un site care merge:")
show_response("https://example.com")
print("Partea 2, show_response pe un site inexistent:")
show_response("http://this-site-does-not-exist.invalid")

# Partea 3: apeluri pentru check_site
print("Partea 3, check_site pe un site care merge:",
      check_site("https://example.com"))
print("Partea 3, check_site pe 404:",
      check_site("https://httpbin.org/status/404"))
print("Partea 3, check_site pe un site inexistent:",
      check_site("http://this-site-does-not-exist.invalid"))

# Partea 4: apelul scan_sites()
print("Partea 4, scan_sites:")
scan_sites()

# Partea 5: apeluri pentru check_headers
print("Partea 5, check_headers cu 2 antete:", check_headers(
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers cu antet scris cu litere mici:", check_headers(
    "https://httpbin.org/response-headers?x-frame-options=DENY"))
print("Partea 5, check_headers pe o pagină fără antete:",
      check_headers("https://httpbin.org/json"))
print("Partea 5, check_headers pe un site inexistent:",
      check_headers("http://this-site-does-not-exist.invalid"))

# Partea 6: apeluri pentru retry_check
print("Partea 6, retry_check pe 200:",
      retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check pe 404:",
      retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check pe 500:",
      retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry_check pe 500 cu 2 încercări:",
      retry_check("https://httpbin.org/status/500", attempts=2))
print("Partea 6, retry_check pe un site inexistent:",
      retry_check("http://this-site-does-not-exist.invalid"))