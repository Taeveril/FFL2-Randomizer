from js import Uint8Array, File, URL, document
from pyscript import web, when, display
import mmap
import hashlib
from FFL2R_io import FFL2_HASH
import FFL2R

thefile = None
rom = mmap.mmap(-1, length=262144, access=mmap.ACCESS_COPY,offset=0)

@when("click", "#cook")
def process():
    global thefile
    global rom
    if thefile == None:
        error_div = web.page["error"]
        error_div.innerText = "No valid Final Fantasy Legend 2 ROM found."
        valid_div = web.page["valid"]
        valid_div.innerText = ""
    else:
        rom.write(thefile.to_bytes())
        valid_div = web.page["valid"]
        valid_div.innerText = "Generating..."
        error_div = web.page["error"]
        error_div.innerText = ""
        results = FFL2R.main(True, rom, None, int(web.page["seed"].value), int(web.page["encounterRate"].value), int(web.page["goldDrops"].value), int(web.page["worldType"].value))
        js_array = Uint8Array.new(len(results[0]))
        js_array.assign(results[0])
        f = File.new([js_array], "ffl2r.gb")
        url = URL.createObjectURL(f)
        download = document.createElement("a")
        download.setAttribute("download", f"Final Fantasy Legend 2 - {str(results[1])}.gb")
        download.setAttribute("href", url)
        download.click()

@when("input", "#rom")
async def loadedROM(event):
    file_list = event.target.files.to_py()
    first_item = file_list.item(0)
    global thefile 
    thefile = await first_item.bytes()
    hashCheck = hashlib.md5(thefile.to_bytes())
    if hashCheck.hexdigest() != FFL2_HASH:
        error_div = web.page["error"]
        error_div.innerText = "MD5 hash mismatch. Invalid Final Fantasy Legend 2 ROM file."
        valid_div = web.page["valid"]
        valid_div.innerText = ""
        thefile = None
    else:
        valid_div = web.page["valid"]
        valid_div.innerText = "Final Fantasy Legend 2 ROM loaded."
        error_div = web.page["error"]
        error_div.innerText = ""