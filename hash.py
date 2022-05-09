import hashlib

# hash a file using md5 and return md5 checksum
def hashFile(fname):
  with open(fname, "rb") as f:
    return hashlib.md5(f.read()).hexdigest()

# hash a string using md5 and return md5 checksum
def hashString(string):
  return hashlib.md5(string.encode('utf-8')).hexdigest()