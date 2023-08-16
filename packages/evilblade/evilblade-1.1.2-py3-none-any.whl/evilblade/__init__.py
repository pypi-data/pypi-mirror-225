from pwn import *
from LibcSearcher import *

'''
明知道是陷阱，
    为什么还要来。
'''
# Convert a number to bytes
n2b = lambda x: str(x).encode()

# Receive data, equivalent to p.recv(x)
rv = lambda x: p.recv(x)

# Receive a line of data, equivalent to p.recvline()
rl = lambda: p.recvline()

# Receive data until a specific string, equivalent to p.recvuntil(s)
ru = lambda s: p.recvuntil(s)

# Send data, equivalent to p.send(s)
sd = lambda s: p.send(s)

# Send data with '\n', equivalent to p.sendline(s)
sl = lambda s: p.sendline(s)

# Send a number with '\n', equivalent to sl(n2b(n))
sn = lambda n: sl(n2b(n))

# Send data after a specific string, equivalent to p.sendafter(t, s)
sa = lambda t, s: p.sendafter(t, s)

# Send a line of data after a specific string, equivalent to p.sendlineafter(t, s)
sla = lambda t, s: p.sendlineafter(t, s)

# Send a number after a specific string, equivalent to sla(t,n2b(n))
sna = lambda t, n: sla(t, n2b(n))

# Start an interactive shell
ia = lambda: p.interactive()

# Convert a list of values to a ROP chain (64-bit)
rop = lambda r: flat([p64(x) for x in r])

# Unpack a 64-bit unsigned integer from bytes
uu64 = lambda data: u64(data.ljust(8, b'\x00'))

##Set your libc, aka libc-set
def libset(libc_val):
    global libc
    libc = ELF(libc_val)

#Set your prosecc and ELF
def setup(p_val):
    global p
    global elf
    p = process(p_val)
    elf = ELF(p_val)
#Establish remote connection
def rsetup(mip, mport):#设置远程连接 remote setup
    if args.P:
        global p
        p = remote(mip,mport)
##Recieve a line of data, and show it for you
def tet():
    #test,测试接收数据    
    p = globals()['p']
    r = ru('\n')
    print('\n----------------\n','add','is >>> ',r,'\n---------------')
    return r

#For 64-bit
#Just like getx32
def getx64(i,j): 
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

#For 32-bit
#After testing with tet(), addresses can be received for the '\xff' format.
#The 'i' parameter represents the start of the received data, while 'j' indicates the end. 
#Usually, 'i' is set to 0, and 'j' is set to -1.
#Continuously adjust the values of 'i' and 'j' until you obtain the desired result.
def getx32(i,j): 
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

#For the hex format
#Just like getx32
def getx(i,j): 
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
    

#For the decimal format
#Just like getx32
def getd(i,j): 
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

#Calculate the base address of libc. "add" is the leaked address, "defname" is the library function name, and "*args" are the excess offsets that need to be subtracted.
def getbase(add,defname,*args):
    #计算libcbase，args作为多余参数相减   get libcbase  
    base = add - libc.sym[defname]
    for num in args:
        base -= num
    print('\nloading...')
    print('\n----------------\nget!your base is >>> ',hex(base),'\n--------------')
    return base

ter = 'NULL'
#If you are unable to directly run GDB, please use the 'terset' to set the terminal according to your situation. Use the output of 'echo $TERM' as the parameter.
def terset(get):
    global ter
    dp('ter',ter)
#Set gdb,aka evil-gdb
#If you need to set a breakpoint, please use 'b address/defname' as the parameter.
def evgdb(*argv):
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
#If the parameter is only 'defname', you will get the offset.
#If there's a second parameter as the base address, you will get the actual address of the function.
def symoff(defname,*args):#计算或者设置偏移symbol's offset
    if(len(args)>0):
        ba = args[0]
        print('\n----------------\nyour ',defname,'offset is >>> ',hex(libc.sym[defname]),'\n---------------')
        print('\n----------------\nyour ',defname,'is in >>> ',hex(ba+libc.sym[defname]),'\n---------------')
        return libc.sym[defname]+ba
    else:
        print('\n---------------\nyour ',defname,'offset is >>> ',hex(libc.sym[defname]),'\n---------------')
        return libc.sym[defname]
#Without PIE, if only "defname", obtain the address of the GOT table.
#With PIE, if only "defname", obtain the offset of the GOT table. Adding the second parameter as the base address will give you the actual GOT table address.
def gotadd(defname,*args):#获取got表地址got'sadd
    if (len(args) > 0):
        return elf.got[defname]+args[0]#有pie的时候
    return elf.got[defname]
#Jusr like gotadd,but obtain the address of the PLT table
def pltadd(defname,*args):#获取got表地址got'sadd
    if (len(args) > 0):
        return elf.plt[defname]+args[0]#有pie的时候
    return elf.plt[defname]

#Just like gotadd,but obtain the address of the SYM table
def symadd(defname,*args):#获取got表地址got'sadd
    if (len(args) > 0):
        return elf.sym[defname]+args[0]#有pie的时候
    return elf.sym[defname]
#Data print
def dp(name,data):#打印数值data print
        print('\n---------------\nyour ',name,' is >>> ',(data),'\n---------------')
#Data print as hex
def dpx(name,data):#hex打印数值data print
        print('\n---------------\nyour ',name,' is >>> ',hex(data),'\n---------------')

'''
因为，   
    我有想要保护的人。
'''

##查库世界

#Set the remote libc library.
def rlibset(defname,add):
    #远程libc设置
    global rlibc
    rlibc = LibcSearcher(defname, add)

#Just like 'getbase', but for remote libc library
def rgetbase(add,defname,*args):
    #计算远程libcbase，args作为多余参数相减   get libcbase  
    base = add - rlibc.dump(defname)
    for num in args:
        base -= num
    print('\nloading...')
    print('\n----------------\nget!your base is >>> ',hex(base),'\n--------------')
    return base
#Just like 'symoff',but for remote libc library
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

#For fmt, but the reliability is not high.
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
