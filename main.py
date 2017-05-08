from itertools import permutations

class task():
    def __init__(self, taskstr, id):
        self.id = id
        self.legend = ''
        self.taskstr = taskstr
        self.cs = []
        self.relationships = []
    def treat(self):
        c = self.taskstr[0]
        if c == 'x': # paralell
            self.legend = 'paralell'
            #print('paralell')
        elif c == 'o': # or
            self.legend = 'or'
            #print('or')
        elif c == 'd':
            self.legend = 'domain'
        elif c == '<':
            self.legend = 'dependence'
        bkp = self.taskstr[1:]
        bkp = bkp.replace('(', '')
        bkp = bkp.replace(')', '')
        bkp = bkp.split(';')
        self.cs = bkp
        #print(bkp)
    def get_groupsets(self):
        if len(self.relationships) > 0:
            return self.relationships
        else:
            return -1


def intersect(a, b):
    #print(a, b)
    """ return the intersection of two lists """
    #first case, we have , in gs a and gs b
    try:
        b_a = a.split(',')
        b_b = b.split(',')
        return list(set(b_a) & set(b_b))
    except:
        pass


def processa(entrada):
    # Independencia: simbolo: *
    # Dependencia: simbolo: <
    #   Strict Dependence(dependencia rigorosa): B so pode executar se A tiver sido, simbolo:
    #   Circumstancial Dependence: B pode executar se A tiver sido ou não executado nenhuma vez
    # Non-coexistence: sets {a} and {b} simbolo: # , conjunto a so pode executar se o b nao existir
    # Uniao: flow ex a, flow b, flow ex a and b

    # Paralelo: + (conjunto)
    # Or: o (conjunto)
    # Exclusive: x (conjunto)
    a = 0
    tasks = []
    for str in entrada:
        tasks.append(task(str, a))
        tasks[a].treat()
        a += 1

    for i in [ k for k in range(0, len(tasks)) if tasks[k].legend != 'domain']: #if tasks[k].legend == 'paralell']:
        for u in [ k for k in range(0, len(tasks)) if tasks[k].legend != 'domain']: #if tasks[k].legend == 'or']:
            if tasks[i].id != tasks[u].id:
                #print(tasks[i].cs, tasks[u].cs)
                true = 0

                groupset_x = tasks[i].cs
                groupset_y = tasks[u].cs
                for choiceset_x in groupset_x:
                    for choiceset_y in groupset_y:
                        #print(choiceset_x, ' ', choiceset_y)
                        intersection = intersect(choiceset_x, choiceset_y)
                        if len(intersection) > 0 and len(choiceset_y) == 1:
                            true += 1
                            if true == len(tasks[u].cs):
                                # Repito o passo e verifico se tem alguma anormalidade...

                                #print(','.join(tasks[u].cs), end='')
                                #print(' -> ', end='')
                                #p = ''.join(tasks[u].cs)
                                tasks[i].relationships += [tasks[u].id]
                                tasks[u].relationships += [tasks[i].id]
                    if true == 1 and tasks[u].legend != 'dependence' and tasks[i].legend != 'dependence':
                        p = ';'.join(tasks[u].cs)
                        q = ';'.join(''.join(a) for a in tasks[i].cs)
                        string = ("Erro: %s nao pode estar contido em dois diferentes choicesets %s" %( p, q))
                        raise Exception(string)

                        #elif len(intersection) > 0 and len(choiceset_x) > 1:
                        #    print(choiceset_x + ' contem ' + choiceset_y)

    list_with_no_virgulas = None
    # gerando os recommendation points
    trocas = 0

    for i in [k for k in range(0, len(tasks)) if tasks[k].legend == 'domain']:
        for u in [k for k in range(0, len(tasks)) if tasks[k].legend == 'dependence']:
            if tasks[i].id != tasks[u].id:
                dependention = tasks[u].cs[0]
                list_with_no_virgulas = tasks[i].cs[0].split(',')
                try:
                    list_with_no_virgulas.remove(dependention)
                    trocas += 1
                except:
                    pass


    print('dominio: ', end='-> ')
    print(list_with_no_virgulas)
    print('conjunto de atividades-> ', end = ' ')
    print( generate_possibilities(list_with_no_virgulas) )




    return tasks

def get_taskbyid(tasks, id):
    for task in tasks:
        if task.id == id:
            return task.cs


def generate_possibilities(lista):
    index = 0
    list = set()
    # adiciono os individuos sozinhos
    for k in lista:
        list.add(k)
    # dps add: a+b, a+d
    for k in range(1, len(lista)):
        list.add(lista[0] + lista[k])


    elem = ''
    for k in range(1, len(lista)):
        elem += str(lista[k])
    elem = lista[0] + elem
    list.add(elem)

    return list
#x(a,b;c,d)", "x(e,f;c,d)", "o(c;d)", "o(e;f)", "d(a,b,c,d)", "<(c;b)"
entrada = ["d(a,b,c,d)", "<(e;a)", "<(c;d)", "o(a;b)", "o(a,b;c,d)"]
try:
    tasks = processa(entrada)
    for task in tasks:
        print(task.cs, end='->')
        for i in range(len(task.relationships)):
            print(get_taskbyid(tasks, task.relationships[i]), end = ',')
        print('')
except Exception as ex:
    print(ex)

# Qual o groupset mais externo
# Dado um gropuset saber em qual choiset ele esta inserido
# Estou fazendo errado..ele esta contindo em um groupset

# Nao pode estar contido em dois, tem que dar um erro caso ele esteja separado em um groupset






