# kubectl agent

This is a simple tool to interact with your cluster using just text. No need to remember kubectl commands, kubectl agent will run them for you.

Here is an example of how it can be used
(I am printing the debug logs below to show the command the agent produced):

```
| | __ _   _ | |__    ___   ___ | |_ | |   __ _   __ _   ___  _ __  | |_ 
| |/ /| | | || '_ \  / _ \ / __|| __|| |  / _` | / _` | / _ \| '_ \ | __|
|   < | |_| || |_) ||  __/| (__ | |_ | | | (_| || (_| ||  __/| | | || |_ 
|_|\_\ \__,_||_.__/  \___| \___| \__||_|  \__,_| \__, | \___||_| |_| \__|
                                                 |___/                   

Ask your cluster some questions? E.g. "How many pods are running in the kube-system namespace?"
Hint: Type // to reset context.
>>list all the pods in the kube-system namespace
DEBUG:main:model called kubectl with arrgs {'command': 'kubectl get pods -n kube-system -o json'}
Here are the pods in the kube-system namespace:
* coredns-565d847f94-p7jqx
* coredns-565d847f94-w7cls
* etcd-kind-control-plane
* kindnet-bbmjq
* kube-apiserver-kind-control-plane
* kube-controller-manager-kind-control-plane
* kube-proxy-smk6k
* kube-scheduler-kind-control-plane
* ubuntu
>>exec into the ubuntu pod and print the contents of /etc/passwd
DEBUG:main:model called kubectl with arrgs {'command': 'kubectl exec -n kube-system ubuntu -- cat /etc/passwd'}

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
```