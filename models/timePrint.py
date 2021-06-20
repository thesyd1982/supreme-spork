def print_timep(time_s):
    if time_s >= 60 and time_s < 3600:
        return "{} m {} s".format(int(time_s / 60), int(time_s % 60))
    elif time_s >= 3600:
        reste_s = int(time_s % 3600)
        return "{} h {} m {} s".format(int(time_s / 3600), int(reste_s / 60), int(reste_s % 60))
    else:
        return "{} s".format(time_s)


if __name__ == "__main__":
	print_timep(3709)