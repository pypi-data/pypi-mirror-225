import pygrab



sess = pygrab.Session()

sess.start_tor()

res = sess.get("http://httpbin.org/get", headers={"User-Agent":"GarlockTheDestroyer"}, enable_js=True)

print(res, '\n\n\n', res.text)

sess.end_tor()

print('\n\n\n')
sess.display_tor_status()