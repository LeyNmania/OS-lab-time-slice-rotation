import java.util.Iterator;
import java.util.Scanner;
import java.util.TreeSet;

public class Process implements Comparable<Process> {
    private String ProcessName;             //进程名
    private int ReachTime;                  //到达时间
    private int ProcessTime;                //处理时间
    private int FinishTime;                 //完成时间
    private int PeriodTime;                 //周转时间
    private int StartTime;                  //开始时间
    private double WeightedPeriodTime;      //带权周转时间
    private int Priority;                   //优先级

    public Process(String processname, int reachTime, int processTime) {
        super();
        ProcessName = processname;
        ReachTime = reachTime;
        ProcessTime = processTime;
    }

    public Process(String processName, int reachTime, int processTime, int priority) {
        super();
        ProcessName = processName;
        ReachTime = reachTime;
        ProcessTime = processTime;
        Priority = priority;
    }

    public int getPriority() {
        return Priority;
    }

    public String getProcessName() {
        return ProcessName;
    }

    public int getReachTime() {
        return ReachTime;
    }

    public int getProcessTime() {
        return ProcessTime;
    }

    public int getFinishTime() {
        return FinishTime;
    }

    public int getPeriodTime() {
        return PeriodTime;
    }

    public void setProcessTime(int processTime) {
        ProcessTime = processTime;
    }

    public void setFinishTime(int finishTime) {
        FinishTime = finishTime;
    }

    public void setPeriodTime(int periodTime) {
        PeriodTime = periodTime;
    }

    public int getStartTime() {
        return StartTime;
    }

    public void setStartTime(int startTime) {
        StartTime = startTime;
    }

    public double getWeightedPeriodTime() {
        return WeightedPeriodTime;
    }

    public void setWeightedPeriodTime(double weightedPeriodTime) {
        WeightedPeriodTime = weightedPeriodTime;
    }

    @Override
    public int compareTo(Process o) {
        // TODO Auto-generated method stub
        if (this.ReachTime > o.ReachTime)
            return 1;
        else if (this.ReachTime < o.ReachTime)
            return -1;
        return 0;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ReachTime;
        return result;
    }

    public void Print() {
        System.out.print(this.ProcessName + " " + this.ReachTime + "  " + this.ProcessTime + "    " + " " + this.StartTime + "  " + this.FinishTime + " " + this.PeriodTime + " ");
        System.out.printf("%.4f", this.WeightedPeriodTime);
        System.out.println();
    }
}

