import requests,time

for i in range(100):
    t = time.time()
    requests.get("https://clcdn.glitch.me")
    print(time.time()-t)