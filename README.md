# keepass4brute.py

ADMinions's KeePass v4 bruteforcer

A threaded Python tool to brute-force passwords on KeePass KDBX 4.x databases using `keepassxc-cli`.

---

## Usage

```bash
python3 keepass4brute.py
```

Then modify the script to point to your `.kdbx` and `wordlist.txt`:
```python
kdbx_file = "/path/to/your/database.kdbx"
wordlist_file = "/path/to/wordlist.txt"
max_threads = 8
```

---

## Legal Disclaimer

This tool is provided for educational and authorized penetration testing purposes only.  
Unauthorized usage against systems without explicit consent is strictly prohibited.

---

## Author

**bobbuilder** – Member of the **ADMinions** https://adminions.ca 
Built for red team engagements, CTFs, and hands-on AD security research.

