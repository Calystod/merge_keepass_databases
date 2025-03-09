from pykeepass import PyKeePass, create_database
from getpass import getpass
from os import listdir
from datetime import datetime
from os.path import isfile, join, dirname, realpath
from dateutil.relativedelta import relativedelta
import sys

_current_dir = dirname(realpath(__file__))
_old_bases_dir = join(_current_dir, "old_bases")
_new_bases_dir = join(_current_dir, "new_bases")

today = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
new_base_name = f"database_{today}.kdbx"

list_files = [f for f in listdir(_old_bases_dir) if isfile(join(_old_bases_dir, f))]

password = getpass()
datas_kp = []

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def calcul_expire_date(last_modification_date):
    new_date = last_modification_date + relativedelta(years=1)

    return new_date

new_keepass = create_database(join(_new_bases_dir, new_base_name), password=password, keyfile=None, transformed_key=None)
root_group = new_keepass.root_group
keep_save = {"groups": {},
             'entries': {}}
list_bds = []
nb_entries = 0
for file in list_files:
    kp = PyKeePass(join(_old_bases_dir, file), password)
    nb_entries += len(kp.entries)
    list_bds.append(kp)

nb_entries_treated = 0
for kp in list_bds:
    for entry in kp.entries:
        try:
            name_group = entry.group.name.strip()
            if entry.group.is_root_group:
                group = root_group
                name_group = group.name.strip()
            else:
                if name_group not in keep_save['groups'].keys():
                    parent_group = new_keepass.root_group
                    if not entry.group.parentgroup.is_root_group:
                        parent_group = entry.group.parentgroup

                    group = new_keepass.add_group(parent_group, name_group, entry.group.icon, entry.group.notes)
                    keep_save['groups'][name_group] = group
                else:
                    group = keep_save['groups'][name_group]
            id = str(name_group) + "/" + entry.title

            if entry.expiry_time:
                expire_date = entry.expiry_time
            else:
                expire_date = calcul_expire_date(entry.mtime)

            if entry.password is None:
                entry.password = ""
            if entry.username is None:
                entry.username = ""
            if id in keep_save['entries'] and keep_save['entries'][id] < entry.mtime:
                added_entry = new_keepass.find_entries(
                title=entry.title,
                username=entry.username,
                first=True,
                group=group,
                recursive=False)

                if added_entry:
                    new_keepass.delete_entry(added_entry)
                    new_keepass.add_entry(group, entry.title, entry.username, entry.password, url=entry.url, notes=entry.notes, tags=entry.tags, expiry_time=expire_date, otp=entry.otp, icon=group.icon, force_creation=True)
                    new_keepass.save()
                keep_save['entries'][id] = entry.mtime
            elif id not in keep_save['entries']:
                added_entry = new_keepass.find_entries(title=entry.title, first=True)

                if not added_entry:
                    new_keepass.add_entry(group, entry.title, entry.username, entry.password, url=entry.url, notes=entry.notes, tags=entry.tags, expiry_time=expire_date, otp=entry.otp, icon=group.icon)
                    new_keepass.save()

                keep_save['entries'][id] = entry.mtime

            nb_entries_treated += 1
            printProgressBar(nb_entries_treated, nb_entries, prefix='Progress:', suffix='Complete', length=50)
        except Exception as e:
            print("Erreur")
            print(entry.title)
            print(e)
            exc_type, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)

print("The new database has", len(keep_save['entries']), "entries")
new_keepass.save()
