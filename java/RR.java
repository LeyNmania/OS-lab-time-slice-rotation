import java.util.Collection;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.TreeSet;

public class RR {
    private TreeSet<Process> process = new TreeSet<Process>();

    public RR() {
        System.out.println("请输入要添加的进程数:");
        Scanner in = new Scanner(System.in);
        int Num = in.nextInt();
        System.out.println("开始初始化进程信息(进程名 到达时间 耗时):");
        for ( int i = 0 ; i < Num ; i++){
            String processname = in.next();
            int reachtime = in.nextInt();
            int processtime = in.nextInt();
            Process p = new Process(processname,reachtime, processtime);
            process.add(p);
        }
    }

    public TreeSet<Process> getProcess() {
        return process;
    }

    public void CarryOut_RR(int Timeperiod){
        LinkedList<Process> Tmp = new LinkedList<>();
        LinkedList<Process> ProcessSeries = new LinkedList<Process>();
        LinkedList<Process> FinsishProcess = new LinkedList<Process>();
        LinkedList<Integer> processtime = new LinkedList<Integer>();
        Iterator<Process> it = this.process.iterator();
        while(it.hasNext()){
            Process p = it.next();
            Tmp.add(p);
            processtime.add(p.getProcessTime());
        }
        int NowTime = Tmp.peekFirst().getReachTime();                       //当前时间
        int NowProcessTime = processtime.pop();
        //第一个进程特殊情况
        Process p = Tmp.pop();
        p.setStartTime(NowTime);
        p.setFinishTime(p.getFinishTime()+Timeperiod);
        p.setPeriodTime(p.getFinishTime() - p.getReachTime());
        p.setWeightedPeriodTime(p.getPeriodTime() * 1.0 / p.getProcessTime());
        NowTime += Timeperiod;
        int FinishTime = p.getFinishTime();                                 //完成时间
        NowProcessTime -= Timeperiod;
        if ( NowProcessTime > 0){
            ProcessSeries.add(p);
            processtime.add(NowProcessTime);
        }else{
            if ( NowProcessTime < 0){
                p.setFinishTime(p.getFinishTime() + NowProcessTime);
                p.setPeriodTime(p.getFinishTime() - p.getReachTime());
                p.setWeightedPeriodTime(p.getPeriodTime() * 1.0 / p.getProcessTime());
                NowTime += NowProcessTime;
                FinishTime = p.getFinishTime();
            }
            FinsishProcess.add(p);
        }
        //时间轮转法
        int len = this.process.size() - 1;
        for ( int i = 0 ; i < len ; i++){
            p = Tmp.pop();
            NowProcessTime = processtime.pop();
            if ( NowTime >= p.getReachTime())
                p.setStartTime(NowTime);
            p.setFinishTime(Timeperiod + FinishTime);
            p.setPeriodTime(p.getFinishTime() - p.getReachTime());
            p.setWeightedPeriodTime(p.getPeriodTime() * 1.0 / p.getProcessTime());
            FinishTime = p.getFinishTime();
            NowTime += Timeperiod;
            NowProcessTime -= Timeperiod;
            if ( NowProcessTime > 0){
                ProcessSeries.add(p);
                processtime.add(NowProcessTime);
            }else{
                if ( NowProcessTime < 0){
                    p.setFinishTime(p.getFinishTime() + NowProcessTime);
                    p.setPeriodTime(p.getFinishTime() - p.getReachTime());
                    p.setWeightedPeriodTime(p.getPeriodTime() * 1.0 / p.getProcessTime());
                    NowTime += NowProcessTime;
                    FinishTime = p.getFinishTime();
                }
                FinsishProcess.add(p);
            }
        }
        while ( !processtime.isEmpty()){
            p = ProcessSeries.pop();
            NowProcessTime = processtime.pop();
            p.setFinishTime(Timeperiod + FinishTime);
            p.setPeriodTime(p.getFinishTime() - p.getReachTime());
            p.setWeightedPeriodTime(p.getPeriodTime() * 1.0 / p.getProcessTime());
            FinishTime = p.getFinishTime();
            NowProcessTime -= Timeperiod;
            if ( NowProcessTime > 0){
                ProcessSeries.add(p);
                processtime.add(NowProcessTime);
            }else{
                if ( NowProcessTime < 0){
                    p.setFinishTime(p.getFinishTime() + NowProcessTime);
                    p.setPeriodTime(p.getFinishTime() - p.getReachTime());
                    p.setWeightedPeriodTime(p.getPeriodTime() * 1.0 / p.getProcessTime());
                    FinishTime = p.getFinishTime();
                }
                FinsishProcess.add(p);
            }
        }

        this.Print(FinsishProcess);
        System.out.printf("平均周转时间:%.4f",this.Avg_ProcessTime(FinsishProcess));
        System.out.println();
        System.out.printf("平均带权周转时间:%.4f",this.Avg_WeightedProcessTime(FinsishProcess));
        System.out.println();
    }

    public double Avg_ProcessTime(Collection<Process> FinsishProcess){                      //平均周转时间
        double avg = 0;
        Iterator<Process> it = this.process.iterator();
        while( it.hasNext()){
            Process p = it.next();
            avg += p.getPeriodTime();
        }
        avg /= this.process.size();
        return avg;
    }

    public double Avg_WeightedProcessTime(Collection<Process> FinsishProcess){                      //平均带权周转时间
        double avg = 0;
        Iterator<Process> it = this.process.iterator();
        while( it.hasNext()){
            Process p = it.next();
            avg += p.getWeightedPeriodTime();
        }
        avg /= this.process.size();
        return avg;
    }

    public void Print(Collection<Process> FinsishProcess){
        System.out.println("            调度示意图");
        System.out.println("进程  到达时间    耗时  开始时间    完成时间    周转时间    带权周转时间");
        Iterator<Process> it = FinsishProcess.iterator();
        while( it.hasNext()){
            Process p = it.next();
            p.Print();
        }
    }

    public static void main(String[] args) {
        // TODO Auto-generated method stub
        RR rr = new RR();
        rr.Print(rr.getProcess());
        System.out.println("请输入时间片：");
        Scanner in = new Scanner(System.in);
        int Timeperiod = in.nextInt();                                      //时间片
        rr.CarryOut_RR(Timeperiod);
        in.close();
    }

}

