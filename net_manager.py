import sqlite3
import cPickle

class NetManager():
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.cur = self.conn.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS '
            'Nets (net_id INTEGER PRIMARY KEY, net_spec TEXT, metas_str TEXT,' 
            'valid_accu REAL, test_accu REAL, comment TEXT)')
        self.dtuple = '(net_id, net_spec, meta_str, valid_accu, test_accu, comment)'
        # self.dbtuple = '(time, task, duration, comment)'

    def save_net(self, net, metas_str, test_accu, valid_accu, 
                 net_spec, comment):
        net_id = [item for item in 
                  self.cur.execute("SELECT MAX(net_id) FROM Nets")][0][0]
        if not net_id:
            net_id = 0
        net_id += 1
        self.cur.execute('INSERT INTO Nets '
                         ' VALUES (?, ?, ?, ?, ?, ?)',
                         (net_id, net_spec, metas_str, test_accu, 
                          valid_accu, comment))
        self.conn.commit()
        with open(self._net_file_name(net_id), 'w+') as f:
            cPickle.dump(net, f)

    def _net_file_name(self, net_id):
        return 'net_data/net_{}.cPickle'.format(net_id)

    def list_nets(self, net_spec=None):
        items = self.cur.execute('SELECT * FROM Nets')
        width = [10, 10, 40, 10, 10, 20]
        fmt = ''.join(['|{{:^{}}}'.format(w) for w in width]) + '|'
        title = self.dtuple[1:-1].split(', ')
        print(fmt.format(*title))
        for net_id, item in enumerate(items):
            item = list(item)
            for i, value in enumerate(item):
                if type(value) == float:
                    item[i] = '{:.2%}'.format(value)
                else:
                    item[i] = str(value)
                if len(item[i]) > width[i]:
                    item[i] = item[i][:-2] + '..'
            print(fmt.format(*item))

    def load_net(self, net_id):
        with open(self._net_file_name(net_id), 'r+') as f:
            return cPickle.load(f)

def test():
    print('----------------Test NetManager-------------------------')
    nm = NetManager('nets_test.sqlite3')
    net = ['hello']
    for i in range(10):
        nm.save_net(net, 'meta_str'+str(i), i/10., i/11., 
                 'test_net', 'comment')
    nm.list_nets()
    net = nm.load_net(12)
    print net