import time
import statistics

class PerformanceTracker:
    def __init__(self):
        # Dicionário para guardar tempos
        self.records = {}
        self.start_time = 0

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self, operation_type):
        elapsed = time.perf_counter() - self.start_time
        if operation_type not in self.records:
            self.records[operation_type] = []
        self.records[operation_type].append(elapsed)

    def print_report(self):
        print("\n" + "="*50)
        print(f"{'OPERAÇÃO':<15} | {'QTD':<8} | {'MÉDIA (s)':<12} | {'MÍN (s)':<10} | {'MÁX (s)':<10}")
        print("-" * 65)
        
        for op, times in self.records.items():
            if not times: continue
            
            avg_t = statistics.mean(times)
            min_t = min(times)
            max_t = max(times)
            count = len(times)
            
            print(f"{op:<15} | {count:<8} | {avg_t:.6f}     | {min_t:.6f}   | {max_t:.6f}")
        print("="*50 + "\n")