#!/usr/bin/python3

import pickle, os, argparse
from datetime import datetime, timedelta

DB_DIRNAME = '/home/dylan/.local/share/timecard'
DB_BASENAME = 'db.pickle'
DB_PATH = DB_DIRNAME + '/' + DB_BASENAME

class Shift:
    def __init__(self, start):
        self.start = start
        self.end = None
    def duration(self):
        return self.end - self.start
    def __str__(self):
        return str(self.end) + " – " + str(self.end) + " ; duration " + str(self.duration())

class Timecard:
    def __init__(self):
        self.shifts = []
        self.shift_active = False

    def total_time(self):
        total = timedelta()
        for shift in self.shifts:
            total += shift.duration()
        return total

    def start(self):
        self.shifts.append(Shift(datetime.now()))
        self.shift_active = True
        return self.shifts[-1]

    def active_shift_start_time(self):
        return self.shifts[-1].start

    def end(self):
        self.shifts[-1].end = datetime.now()
        self.shift_active = False
        return self.shifts[-1]

    def clear(self):
        self.__init__()

    def get_status(self):
        if self.shift_active:
            return "shift active; started at " + str(self.shifts[-1].start)
        else:
            return "no shift active"

def check_db_file():
    if not os.path.isdir(DB_DIRNAME):
        os.makedirs(DB_DIRNAME)
    if not os.path.isfile(DB_PATH):
        # create emtpy timecard
        with open(DB_PATH, 'wb') as f:
            pickle.dump(Timecard(), f)
    return open(DB_PATH, 'rb')

def open_db():
    with check_db_file() as f:
        db = pickle.load(f)
    return db

def save_and_close_db(db):
    check_db_file()
    with open(DB_PATH, 'wb') as db_file:
        pickle.dump(db, db_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Track your work shifts')
    parser.add_argument('action', type=str, choices=['status', 'start', 'end', 'list', 'total', 'clear'], help='Action to perform')
    args = parser.parse_args()
    # open up db
    db = open_db()
    if args.action == 'status':
        print(db.get_status())
    elif args.action == 'start':
        new_shift = db.start()
        print("shift started at " + str(new_shift.start))
    elif args.action == 'end':
        if db.shift_active:
            new_shift = db.end()
            print("shift ended at " + str(new_shift.end) + "; duration " + str(new_shift.duration()))
        else:
            print("error: no shift active")
    elif args.action == 'list':
        if len(db.shifts) == 0:
            print("no shifts recorded")
        else:
            for shift in db.shifts:
                print(shift)
            print("total: " + str(db.total_time()))
    elif args.action == 'total':
        print("total: " + str(db.total_time()))
    elif args.action == 'clear':
        db.clear()
        print("all shifts cleared")
    save_and_close_db(db)
