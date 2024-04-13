class Trie(object):
    def __init__(self):
        self.trie = {}
        self.count = 0

    def __repr__(self):
        return str(self.trie)

    def add(self, word):
        t = self.trie
        for w in word:
            if w not in t:
                t[w] = {'count': 0}
            t[w]['count'] += 1
            t = t[w]

        self.count += 1
        t['end'] = 1

    def delete(self, word):
        if not self.search(word):
            return False

        t = self.trie
        for w in word:
            t = t[w]
            t['count'] -= 1

        self.count -= 1
        t['end'] = 0

    def search(self, word):
        t = self.trie
        for w in word:
            if w not in t:
                return False
            t = t[w]
        if t.get('end') == 1:
            return True
        return False

    def __contains__(self, item):
        return self.search(item)

    def __len__(self):
        return self.count
