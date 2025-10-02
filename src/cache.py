# src/cache.py
from collections import OrderedDict

# -----------------------
# LRU Cache
# -----------------------
class LRUCache:
    def __init__(self, capacity=100):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.hits += 1
            value = self.cache.pop(key)
            self.cache[key] = value  # mover al final = más reciente
            return value
        else:
            self.misses += 1
            return None

    def set(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # elimina el menos usado
        self.cache[key] = value

    def put(self, key, value):
        """Método de compatibilidad con main_lru.py"""
        self.set(key, value)

# -----------------------
# LFU Cache
# -----------------------
class LFUCache:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.cache = {}
        self.freq = {}
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.hits += 1
            self.freq[key] += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def set(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.freq[key] += 1
        else:
            if len(self.cache) >= self.capacity:
                # eliminar el menos usado
                min_freq_key = min(self.freq, key=lambda k: self.freq[k])
                del self.cache[min_freq_key]
                del self.freq[min_freq_key]
            self.cache[key] = value
            self.freq[key] = 1

    def put(self, key, value):
        """Método de compatibilidad con main_lfu.py"""
        self.set(key, value)
