import pymysql.cursors
import json
import serial
import time

# MySQL 연결 정보
mysql_host = '34.64.46.181'
mysql_user = 'aznoca'
mysql_password = 'Zxc3810+'
mysql_db = 'DHT'

create_measure_table_query = '''
CREATE TABLE IF NOT EXISTS `Measure` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `humi` FLOAT,
    `temp` FLOAT,
    `ground_humi` FLOAT,
    `timestamp` DATETIME
);
'''

def dhtserial():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    try:
        data = ser.readline()
        decoded_data = data.decode('utf-8')
        parsed_values = json.loads(decoded_data)
    except Exception as e:
        print(f"Error reading and decoding serial data: {e}")
        parsed_values = {}
    finally:
        ser.close()
    return parsed_values

def db_insert(data):
    # MySQL 연결 설정
    conn = pymysql.connect(host=mysql_host,
                           user=mysql_user,
                           password=mysql_password,
                           db=mysql_db,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    now = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()

    # Measure 테이블 생성 쿼리
    cursor.execute(create_measure_table_query)
    conn.commit()

    try:
        # 쿼리 실행
        insert_query = '''INSERT INTO `Measure` (`humi`, `temp`, `ground_humi`, `timestamp`) VALUES (%s, %s, %s, %s)'''
        cursor.execute(insert_query, (data['humi'], data['temp'], data['ground_humi'], now))
        conn.commit()
        print(f"Data inserted successfully: {data}")
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    while True:
        # 아두이노에서 전송된 데이터 읽어오기
        data = dhtserial()

        # MySQL에 데이터 삽입
        if data:
            db_insert(data)

        # 60초 대기
        time.sleep(1798)
