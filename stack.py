class Process_Stack(object):
    def __init__(self):
        self.stack = {}
    def add(self, process_name, process_ID):
        if process_name in self.stack:
            self.stack[process_name].append(process_ID)
        else:
            self.stack[process_name]=[process_ID]
    def delete(self, process_name):
        if process_name in self.stack:
            process_ID = self.stack[process_name].pop(-1)
            if len(self.stack[process_name]) == 0:
                self.stack.pop(process_name)
            return [True, process_ID]
        else:
            return [False, 0]
    def statistics(self):
        process_list = list(self.stack.keys())
        report = 'Stats:'
        if len(process_list) == 0:
            report += ' None'
        else:
            for process in process_list:
                report += '\n'
                report += f"{process}: {len(self.stack[process])}"
        return report
    def clear(self):
        process_list = list(self.stack.keys())
        report = 'Clear:'
        clear_list = []
        for process in process_list:
            report += '\n'
            report += f"{process}: {len(self.stack[process])}"
            for i in range(len(self.stack[process])):
                a,b = self.delete(process)
                clear_list.append(b)
        return report, clear_list



