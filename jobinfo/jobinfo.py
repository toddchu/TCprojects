import os
import re


class JobApplied:
    jobs_list = []
    jobs_searched_list = []
    jobs_search_value = ''

    def __init__(self, folder_name, file_name):
        self.folder_name = folder_name
        self.file_name = file_name
        self.company = ''
        self.apply_date = ''
        self.position = ''
        self.split_name = file_name

    @property
    def split_name(self):
        return

    @split_name.setter
    def split_name(self, file_name):
        p = re.compile(r"([\w|\s|\.|\-\_]+)([\d]+\-[\d]+\-[\d]+)([\w|\s|\.|\-\_]+)")
        matches = p.finditer(file_name)
        for match in matches:
            self.company = match.group(1).strip(' ')
            self.apply_date = match.group(2)
            self.position = match.group(3).strip(' ')

    @staticmethod
    def new(folder_name, file_name):
        p = JobApplied(folder_name, file_name)
        JobApplied.jobs_list.append(p)
        return p

    @staticmethod
    def get_key_val_pair(p, sort_by):
        if sort_by is 'Date':
            key = f'{p.apply_date}'
        elif sort_by is 'Company':
            key = f'{p.company}'
        elif sort_by is 'Position':
            key = f'{p.position}'
        elif sort_by is 'Folder':
            key = f'{p.folder_name}'
        elif sort_by is 'File':
            key = f'{p.file_name}'
        else:
            print(f'get_key_val_pair(): Unknown flag: "{sort_by}"')
            return []

        return [key, p.__repr__()]

    @staticmethod
    def jobs_sorted_by(sort_by, reverse_flag=False, searched_list_flag=False):
        if searched_list_flag is True:
            p_list = JobApplied.jobs_searched_list
        else:
            p_list = JobApplied.jobs_list

        # Generate a new list by placing key and value
        name_tmp_list = []
        for p in p_list:
            name_tmp_list.append(JobApplied.get_key_val_pair(p, sort_by))

        # Sort the lst
        name_tmp_list.sort(key=lambda x: x[0], reverse=reverse_flag)

        # split the value at index 1 to a new list
        name_list = []
        i = 1
        for name_tmp in name_tmp_list:
            m = name_tmp[1].split(', ')
            m.insert(0, f'{i}')
            i += 1
            name_list.append(m)

        return name_list

    @staticmethod
    def jobs_search_by(sort_by, name, reverse_flag=False):
        JobApplied.jobs_searched_list.clear()

        if len(name) > 0:
            for p in JobApplied.jobs_list:
                if name.upper() in p.company.upper():
                    JobApplied.jobs_searched_list.append(p)

            name_list = JobApplied.jobs_sorted_by(sort_by, reverse_flag, True)
            return name_list
        else:
            return []

    @staticmethod
    def set_search_value(name):
        JobApplied.jobs_search_value = name

    @staticmethod
    def get_search_value():
        return JobApplied.jobs_search_value

    def __repr__(self):
        return f"{self.apply_date}, {self.company}, {self.position}, {self.folder_name}, {self.file_name}"


class JobInfo(JobApplied):
    def __init__(self, path):
        self.job_applied = JobApplied("HEAD", "HEAD")

        for root, dirs, files in os.walk(path):
            for dd in dirs:
                folder_name = os.path.join(root, dd)
                date = JobInfo.check_folder(folder_name)

                if date is not None:
                    for r, d, fs in os.walk(folder_name):
                        for f in fs:
                            # file_name = os.path.join(r, f)
                            self.job_applied.new(r, f)

    @staticmethod
    def check_folder(folder_name):
        p = re.compile(r'([\d]+\-[\d]+\-[\d]+)')
        matches = p.finditer(folder_name)
        for m in matches:
            return m.group(1)


if __name__ == "__main__":
    jobs = JobInfo("c:\\Users\\toddd\\Home\\MyGit\\TCprojects\\jobinfo\\JobApplied")

    sort_list = jobs.jobs_sorted_by("Company")
    for ss in sort_list:
        print(ss)
    print()

    jobs.set_search_value('ve')
    search_value = jobs.get_search_value()
    search_list = jobs.jobs_search_by('Date', search_value)
    for ss in search_list:
        print(ss)

