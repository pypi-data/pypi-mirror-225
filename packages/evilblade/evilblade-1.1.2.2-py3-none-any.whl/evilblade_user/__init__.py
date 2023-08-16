from pwn import *
from LibcSearcher import *

'''
明知道是陷阱，
    为什么还要来。
'''

n2b = lambda x    : str(x).encode()
rv  = lambda x    : p.recv(x)
rl  = lambda     :p.recvline()
ru  = lambda s    : p.recvuntil(s)
sd  = lambda s    : p.send(s)
sl  = lambda s    : p.sendline(s)
sn  = lambda s    : sl(n2b(n))
sa  = lambda t, s : p.sendafter(t, s)
sla = lambda t, s : p.sendlineafter(t, s)
sna = lambda t, n : sla(t, n2b(n))
ia  = lambda      : p.interactive()
rop = lambda r    : flat([p64(x) for x in r])
uu64=lambda data :u64(data.ljust(8,b'\x00'))

##初始化世界
def libset(libc_val):#设置libc libc-set
    global libc
    libc = ELF(libc_val)

def setup(p_val):#设置程序 
    global p
    global elf
    p = process(p_val)
    elf = ELF(p_val)

def rsetup(mip, mport):#设置远程连接 remote setup
    if args.P:
        global p
        p = remote(mip,mport)
##接收世界
def tet():
    #test,测试接收数据    
    p = globals()['p']
    r = ru('\n')
    print('\n----------------\n','add','is >>> ',r,'\n---------------')
    return r

def getx64(i,j): 
    #\xff格式，测试差不多之后可以得到了    
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('getx64',r)
        r = u64(r.ljust(8,b'\0'))
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r
    else:
        r = (ru('\n'))[:j]
        dp('getx64',r)
        r = u64(r.ljust(8,b'\0'))
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r

def getx32(i,j): 
    #\xff格式，测试差不多之后可以得到了    
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('getx32',r)
        r = u32(r.ljust(4,b'\0'))
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r
    else:
        r = (ru('\n'))[:j]
        dp('getx32',r)
        r = u32(r.ljust(4,b'\0'))
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r

def getx(i,j): 
    #0xff格式,测试差不多之后可以得到了    
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('geti',r)
        r = int(r,16)
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r
    else:
        r = (ru('\n'))[:j]
        dp('geti',r)
        r = int(r,16)
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r
    

def getd(i,j): 
    #整数格式,测试差不多之后可以得到了    
    if i != 0:
        r = (ru('\n'))[i:j]
        dp('geti',r)
        r = int(r,10)
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r
    else:
        r = (ru('\n'))[:j]
        dp('geti',r)
        r = int(r,10)
        print('\n----------------\n','add','is >>> ',hex(r),'\n---------------')
        return r
    
'''
只攻不防，
    天下无双—————
        魔刀千刃。
'''
##计算世界

def getbase(add,defname,*args):
    #计算libcbase，args作为多余参数相减   get libcbase  
    base = add - libc.sym[defname]
    for num in args:
        base -= num
    print('\nloading...')
    print('\n----------------\nget!your base is >>> ',hex(base),'\n--------------')
    return base

ter = 'NULL'
def terset(get):
    global ter
    #如果不能直接运行gdb请根据自己的情况用terset设置终端
    #运行echo $TERM结果替换alacritty
    ter = get
    dp('ter',ter)

def evgdb(*argv):#设置gdb evil-gdb
    p = globals()['p']
    ter = globals()['ter']
    #获取全局变量值
    dp('gdbter',ter)
    if ter!='NULL':
        context.terminal = [ter, '-e']
    if args.G:
        if(len(argv)==0):
            gdb.attach(p)
        else:
            gdb.attach(p,argv[0])

def symoff(defname,*args):#计算或者设置偏移symblol's offset
    if(len(args)>0):
        ba = args[0]
        print('\n----------------\nyour ',defname,'offset is >>> ',hex(libc.sym[defname]),'\n---------------')
        print('\n----------------\nyour ',defname,'is in >>> ',hex(ba+libc.sym[defname]),'\n---------------')
        return libc.sym[defname]+ba
    else:
        print('\n---------------\nyour ',defname,'offset is >>> ',hex(libc.sym[defname]),'\n---------------')
        return libc.sym[defname]

def gotadd(defname,*args):#获取got表地址got'sadd
    if (len(args) > 0):
        return elf.got[defname]+args[0]#有pie的时候
    return elf.got[defname]

def pltadd(defname,*args):#获取got表地址got'sadd
    if (len(args) > 0):
        return elf.plt[defname]+args[0]#有pie的时候
    return elf.plt[defname]

def symadd(defname,*args):#获取got表地址got'sadd
    if (len(args) > 0):
        return elf.sym[defname]+args[0]#有pie的时候
    return elf.sym[defname]

def dp(name,data):#打印数值data print
        print('\n---------------\nyour ',name,' is >>> ',(data),'\n---------------')

def dpx(name,data):#hex打印数值data print
        print('\n---------------\nyour ',name,' is >>> ',hex(data),'\n---------------')

'''
因为，   
    我有想要保护的人。
'''

##查库世界

def rlibset(defname,add):
    #远程libc设置
    global rlibc
    rlibc = LibcSearcher(defname, add)


def rgetbase(add,defname,*args):
    #计算远程libcbase，args作为多余参数相减   get libcbase  
    base = add - rlibc.dump(defname)
    for num in args:
        base -= num
    print('\nloading...')
    print('\n----------------\nget!your base is >>> ',hex(base),'\n--------------')
    return base

def rsymoff(defname,*args):#计算或者设置偏移symblol's offset
    if(len(args)>0):
        ba = args[0]
        print('\n----------------\nyour ',defname,'offset is >>> ',hex(rlibc.dump(defname)),'\n---------------')
        print('\n----------------\nyour ',defname,'is in >>> ',hex(ba+rlibc.dump(defname)),'\n---------------')
        return rlibc.dump(defname)+ba
    else:
        print('\n---------------\nyour ',defname,'offset is >>> ',hex(rlibc.dump(defname)),'\n---------------')
        return rlibc.dump(defname)

#攻击世界

def fmt(offset,begin,end,size,written):
    #fmt利用
    payload = fmtstr_payload(offset,{begin: end},write_size = size,numbwritten=written)
    return payload
'''
    offset（int） - 您控制的第一个格式化程序的偏移量
    字典（dict） - 被写入地址对应->写入的数据，可多个对应{addr: value, addr2: value2}
    numbwritten（int） - printf函数已写入的字节数
    write_size（str） - 必须是byte，short或int。告诉您是否要逐字节写入，短按short或int（hhn，hn或n）
'''
