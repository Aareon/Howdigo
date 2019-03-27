from .core import time, csv

# acts as timing mechanism during streaming, there may be a much easier way of doing this 
def time_tracker(max_wait, from_stream_q, to_main_q):
    stream_time = 0
    while True:
        while from_stream_q.qsize():
            try:
                info = from_stream_q.get(0)
                try:
                    if info['new_stream']:
                        stream_time = 0
                except KeyError:
                    pass
            except:
                pass
        if stream_time > max_wait:
            to_main_q.put({'done': True})
            break

        time.sleep(1)
        to_main_q.put({'update_wheel': True})
        stream_time += 1



def write_csv_file(f, data):
    headers = []
    for header,value in data[0].items():
        headers.append(header)

    csv_writer = csv.DictWriter(f, fieldnames=['id']+headers, delimiter=',',lineterminator='\n')
    csv_writer.writeheader()
    for i, row in enumerate(data):
        row['id'] = i
        csv_writer.writerow(row)
        # f.flush()
    f.close()
