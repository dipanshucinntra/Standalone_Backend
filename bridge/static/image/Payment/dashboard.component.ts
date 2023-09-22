import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { BridgeService } from '../modules/service/bridge.service';
// import { Chart } from 'node_modules/chart.js';
import Chart from 'chart.js/auto';
import { HttpClient } from '@angular/common/http';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { Bridge } from '../bridge';
import { DatePipe } from '@angular/common';
declare var $: any;
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  UserName: any;
  SalesEmployeeCode: any;
  barChartdata: any;
  barChartdata2: any;
  top5customerbar: any;
  top5bp: any[] = [];
  barChartdata3: any;
  revanue: any;
  sales: any;
  sales_diff: any;
  notification: any;
  baseUrl2: any;
  nodata: boolean = false;
  nodata_top5itembyamount: boolean = false;
  nodata_movingitems: boolean = true;
  bestselling:boolean=false;
  bridges: Bridge[] = [];
  role: any;

  Lead: any;
  Need: any;
  Quotation: any;
  Negotiation: any;
  Order: any;

  dateObj = new Date();
  time = this.dateObj.toLocaleTimeString();
  month2 = this.dateObj.getMonth() + 1;
  month = (this.month2 < 10 ? '0' : '') + this.month2;
  day = (this.dateObj.getDate() < 10 ? '0' : '') + this.dateObj.getDate();
  year = this.dateObj.getUTCFullYear();
  //  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  newdate = this.year + "-" + this.month + "-" + this.day;

  inputElementTime = ("0" + this.dateObj.getHours()).slice(-2) + ":" + ("0" + this.dateObj.getMinutes()).slice(-2);


  Weekdate: any;
  monthlydate: any;
  yearlydate: any;

  constructor(private modalService: NgbModal, public datepipe: DatePipe, private bridgeService: BridgeService, private route: Router, private http: HttpClient) {
    this.baseUrl2 = this.bridgeService.baseUrl2;
  }

  ngOnInit(): void {


    this.bridgeService.autoCall();

    this.UserName = sessionStorage.getItem('UserName');
    this.role = sessionStorage.getItem('role');
    this.SalesEmployeeCode = sessionStorage.getItem('SalesEmployeeCode');
    // console.log(this.SalesEmployeeCode);
    if (this.UserName == undefined) {
      this.route.navigate(['/login']);
    }
    this.selectedDevice=this.SalesEmployeeCode;


    this.http.post(this.baseUrl2 + '/employee/dashboard', { "SalesEmployeeCode": this.SalesEmployeeCode }).toPromise().then((data: any) => {
      this.revanue = data.data[0].amount;
      this.sales = data.data[0].sale;
      this.sales_diff = data.data[0].sale_diff;
      this.notification = data.data[0].notification;
    });

    this.alterfunction();
    this.CharFunction();


    $(document).mouseup(function (e: { target: any; }) {
      var popup = $(".showNoti");
      if (!$('.bellclass').is(e.target) && !popup.is(e.target) && popup.has(e.target).length == 0) {
        popup.hide();
      }
    });

    $(document).ready(function () {
      $('.showNoti').hide()
    });
    this.getBridge();


    // weekly sorting date
    this.Weekdate = this.datepipe.transform(new Date(this.dateObj.getTime() - 7 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd')
    // console.log(this.datepipe.transform(new Date(this.dateObj.getTime() - 7 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd'));
    console.log('this.Weekdate',this.Weekdate);

    // monthly sorting date
    var lastDay = new Date(this.dateObj.getFullYear(), this.dateObj.getMonth() - 1, 0);
    // console.log(this.datepipe.transform(lastDay, 'yyyy-MM-dd'))
    this.monthlydate = this.datepipe.transform(lastDay, 'yyyy-MM-dd');

    // year sorting date
    var lastYear = new Date(this.dateObj.getFullYear() - 1, 0);
    // console.log(this.datepipe.transform(lastYear, 'yyyy-MM-dd'))
    this.yearlydate = this.datepipe.transform(lastYear, 'yyyy-MM-dd');


  }


  getBridge(): void {
    this.bridgeService.getempall().subscribe(
      (data: Bridge[]) => {
        this.bridges = data;
        // console.log('employee list', this.bridges);
        for (let i = 0; i < this.bridges.length; i++) {
          if (this.bridges[i]['SalesEmployeeCode'] == '-1') {
            this.bridges.splice(i, 1);
          }
          if (this.bridges[i]['SalesEmployeeCode'] == '') {
            this.bridges.splice(i, 1);
          }
        }


      },
      (err) => {
        console.log(err);

      }
    );
  }
  selectedDevice = '';
  Lead1: any;
  Need1: any;
  Quotation1: any;
  Negotiation1: any;
  Order1: any;

  barCharttopcustomer:any;

  dashboardemployeecode(code: any) {
    // console.log('code----', code)
    // this.SalesEmployeeCode=code;


    this.fastload = true;
    this.nodata = true;
    if(this.lineChart != undefined){
      this.lineChart.destroy();
      this.barChart3.destroy();
      this.barChart2.destroy();
      }
    this.http.post(this.baseUrl2 + '/employee/opportunity_bystage', { "SalesEmployeeCode": code }).toPromise().then((data: any) => {

      this.barChartdata3 = data;

      if (data['data'].length > 0) {
        this.nodata = false;
      }
      this.Lead = this.barChartdata3.data[0].Lead;
      this.Need = this.barChartdata3.data[0].NeedAnalysis;
      this.Quotation = this.barChartdata3.data[0].Quotation;
      this.Negotiation = this.barChartdata3.data[0].Negotiation;
      this.Order = this.barChartdata3.data[0].Order;
      if (data['status'] == 200) {
        this.fastload = false;
      }

      this.lineChart = new Chart("lineChart", {

      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
          {
            label: 'Stages',
            data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
            // data: [0,0,0,0],

            backgroundColor: '#95B5FF',
            borderColor: '#95B5FF',
            tension: 0.4,
          },
          {
            label: 'Stages',
            data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
            backgroundColor: '#4A79E4',
            borderColor: '#4A79E4',
            tension: 0.4,
          },

        ]
      },
      options: {
        events: [],

        plugins: {
          legend: {
            display: false,
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: {
              display: false,
              drawBorder: false,
            }
          },
          y: {
            beginAtZero: true,
            grid: {
              display: false,
              drawBorder: false
            }
          }
        }
      }

    });
      // this.lineChart.data.datasets = [{
      //   label: 'Stages',
      //   data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
      //   backgroundColor: '#95B5FF',
      //   borderColor: '#95B5FF',
      //   tension: 0.4,
      // }];
      // this.lineChart.update();
    });


    this.nodata_top5itembyamount = true;
    if(this.barCharttopcustomer != undefined){
    this.barCharttopcustomer.destroy();
    }
    this.http.post(this.baseUrl2 + '/employee/top5bp', { "SalesPersonCode": code }).toPromise().then((data: any) => {
      this.top5bp = data.data;

      if (data['data'].length > 0) {
        this.nodata_top5itembyamount = false;

        this.TopcustmerCardName = [];
        this.TopcustmerTotal = [];
      for (let i = 0; i < this.top5bp.length; i++) {
        this.TopcustmerCardName.push(this.top5bp[i].CardName);
        this.TopcustmerTotal.push(this.top5bp[i].Total);
      }

      // this.barCharttopcustomer = new Chart(document.querySelector<HTMLCanvasElement>(`#barCharttopcustomer`)!, {
        this.barCharttopcustomer = new Chart("barCharttopcustomer", {
        type: 'bar',
        data: {
          // labels: ['laptop', 'Mobile',],
          labels: this.TopcustmerCardName,
          datasets: [{
            label: 'Best Selling Item By Sales Amount',
            //data: [20,30],
            data: this.TopcustmerTotal,
            borderRadius: 15,
            backgroundColor: [
              '#65B0F6',
              '#65B0F6',
              '#65B0F6',
              '#65B0F6',
              '#65B0F6'
            ],
            borderColor: [
              '#65B0F6',
              '#65B0F6',
              '#65B0F6',
              '#65B0F6',
              '#65B0F6'
            ],
            borderWidth: 1,
            barThickness: 10,
          }]
        },
        options: {
          events: [],
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              grid: {
                display: false,
                drawBorder: false
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                display: false,
                drawBorder: false,
              }
            }
          }
        }

    });


    }
    });





    if(this.barChart2 != undefined){
      this.barChart2.destroy();
      }
      this.bestselling = true;
    this.http.post(this.baseUrl2 + '/employee/top5itembyamount',{ "SalesPersonCode": code }).toPromise().then((data: any) => {
      this.barChartdata2 = data;
      this.labels3 = [];
      this.datas3 = [];
      this.bestSellingItem = [];
      this.bestSellingCardName = [];
      if (data['data'].length > 0) {
        this.bestselling = false;
      }
      for (let i = 0; i < this.barChartdata2.data.length; i++) {
        this.bestSellingItem.push(this.barChartdata2.data[i].ItemName);
        this.bestSellingCardName.push(this.barChartdata2.data[i].Total);
        // bestSellingItem:any[]=[];
        // bestSellingCardName:any[]=[];
        this.labels3 = this.barChartdata2.data[i].ItemName + ",";
        this.datas3 = this.barChartdata2.data[i].Total + ",";
      }

      console.log('sellingItem',this.bestSellingItem);
      console.log('card Name',this.bestSellingCardName);
      // this.labels3 = this.labels3.replace('undefined', '').slice(0, -1);
      // this.datas3 = this.datas3.replace('undefined', '').slice(0, -1);

      // this.labels3 = this.labels3.split(',');

      // this.datas3 = this.datas3.split(',');



      // this.barChart2.data.datasets = [{
      //   labels: this.labels3,
      //   data: this.datas3,
      //       borderRadius: 15,
      //       backgroundColor: [
      //         'rgba(255, 99, 132, 1)',
      //         'rgba(54, 162, 235, 1)',
      //         'rgba(255, 206, 86, 1)',
      //         'rgba(153, 102, 255, 1)',
      //         'rgba(255, 159, 64, 1)'
      //       ],
      //       borderColor: [
      //         'rgba(255, 99, 132, 1)',
      //         'rgba(54, 162, 235, 1)',
      //         'rgba(255, 206, 86, 1)',
      //         'rgba(153, 102, 255, 1)',
      //         'rgba(255, 159, 64, 1)'
      //       ],
      //       borderWidth: 1,
      //       barThickness: 10,
      // }];
      // this.barChart2.update();



      this.barChart2 = new Chart("barChart2", {
        type: 'bar',
        data: {
          // labels: [this.barChartdata2.data[0].ItemName, this.barChartdata2.data[1].ItemName, this.barChartdata2.data[2].ItemName, this.barChartdata2.data[3].ItemName, this.barChartdata2.data[4].ItemName],
          labels: this.bestSellingItem,
          datasets: [{
            label: 'Best Selling Item By Sales Amount',
            // data: [this.barChartdata2.data[0].Total, this.barChartdata2.data[1].Total, this.barChartdata2.data[2].Total, this.barChartdata2.data[3].Total, this.barChartdata2.data[4].Total],
            data: this.bestSellingCardName,
            borderRadius: 15,
            backgroundColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1,
            barThickness: 10,
          }]
        },
        options: {
          events: [],
          plugins: {
            legend: {
              display: false,

            }
          },
          scales: {
            x: {
              beginAtZero: true,
              grid: {
                display: false,
                drawBorder: false
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                display: false,
                drawBorder: false
              }
            }

          }
        }
      });
    });


    this.fastload = true;
    this.nodata = true;
    // console.log('this.SalesEmployeeCode2',this.SalesEmployeeCode);
    // console.log('--------this.Lead1-------',this.Lead1);
    this.http.post(this.baseUrl2 + '/employee/opportunity_bystage', { "SalesEmployeeCode": code }).toPromise().then((data: any) => {
      this.barChartdata3 = data;
      // console.log(this.barChartdata3);
      if (data['data'].length > 0) {
        this.nodata = false;
      }
      this.Lead = this.barChartdata3.data[0].Lead;
      this.Need = this.barChartdata3.data[0].NeedAnalysis;
      this.Quotation = this.barChartdata3.data[0].Quotation;
      this.Negotiation = this.barChartdata3.data[0].Negotiation;
      this.Order = this.barChartdata3.data[0].Order;
      if (data['status'] == 200) {
        this.fastload = false;
      }

      // this.lineChart.data.datasets = [{
      //   label: 'Stages',
      //   data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
      //   backgroundColor: '#95B5FF',
      //   borderColor: '#95B5FF',
      //   tension: 0.4,
      // }];
      // this.lineChart.update();






      // this.barChart3.data.datasets = [{
      //   labels: ['', '', '', '', ''],
      //   data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
      //         borderRadius: 15,
      //         backgroundColor: [
      //           '#95B5FF',
      //           '#95B5FF',
      //           '#95B5FF',
      //           '#95B5FF',
      //           '#95B5FF'
      //         ],
      //         borderColor: [
      //           '#95B5FF',
      //           '#95B5FF',
      //           '#95B5FF',
      //           '#95B5FF',
      //           '#95B5FF'
      //         ],
      //         borderWidth: 1,
      //         barThickness: 10,
      // }];
      // this.barChart3.update();

      this.barChart3 = new Chart("barChart3", {
        type: 'bar',
        data: {
          labels: ['', '', '', '', ''],
          datasets: [
            {
              label: 'Stages',
              data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
              borderRadius: 15,
              backgroundColor: [
                '#95B5FF',
                '#95B5FF',
                '#95B5FF',
                '#95B5FF',
                '#95B5FF'
              ],
              borderColor: [
                '#95B5FF',
                '#95B5FF',
                '#95B5FF',
                '#95B5FF',
                '#95B5FF'
              ],
              borderWidth: 1,
              barThickness: 10,
            },
            {
              label: 'Stages',
              data: [10, 11, 34, 23, 34],
              borderRadius: 15,
              backgroundColor: [
                '#4A79E4',
                '#4A79E4',
                '#4A79E4',
                '#4A79E4',
                '#4A79E4'
              ],
              borderColor: [
                '#4A79E4',
                '#4A79E4',
                '#4A79E4',
                '#4A79E4',
                '#4A79E4'
              ],
              borderWidth: 1,
              barThickness: 10,
            },
            {
              label: 'Stages',
              data: [4, 6, 8, 9, 5],
              borderRadius: 15,
              backgroundColor: [
                '#FFA63D',
                '#FFA63D',
                '#FFA63D',
                '#FFA63D',
                '#FFA63D'
              ],
              borderColor: [
                '#FFA63D',
                '#FFA63D',
                '#FFA63D',
                '#FFA63D',
                '#FFA63D'
              ],
              borderWidth: 1,
              barThickness: 10,
            },
          ]
        },
        options: {
          events: [],
          plugins: {
            legend: {
              display: false,
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              grid: {
                display: false,
                drawBorder: false,
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                display: false,
                drawBorder: false
              }
            }
          }
        }

      });
    });

  }



  alterfunction() {
    var alerted = sessionStorage.getItem('alerted') || '';
    if (alerted != 'Yes') {
      $(".alert-primary").fadeIn(100);
      sessionStorage.setItem('alerted', 'Yes');
    }
    setTimeout(function () {
      $(".alert-primary").fadeOut(1000);
    }, 3000);

  }
  lavels: any;
  datas: any;



  labels3: any;
  datas3: any;

  NotMovingItemsCount: any;
  SlowItemsCount: any;
  FastItemsCount: any;



  fastload: boolean = false;
  top5customer: boolean = false;
  arr1: any = []

  lineChart: any;
  pieChart:any;
  barChart2:any;
  barChart3:any;

  TopcustmerCardName: any[] = [];
  TopcustmerTotal: any[] = [];

  bestSellingItem:any[]=[];
  bestSellingCardName:any[]=[];

  xpieValues2:any[]=[];
    ypieValues2:any[]=[];
    barpieColors:any[]=[];

  CharFunction() {
    // Bar chart

    this.top5customer = true;

   this.dashboardemployeecode(this.SalesEmployeeCode);
    // Bar chart2
    // this.SalesEmployeeCode










    // Bar chart2






    // Bar chart3

    // console.log('SalesEmployeeCode',this.SalesEmployeeCode);


    // Line Chart





    // Pie Chart

    // this.http.get(this.baseUrl2+'/employee/movingitems').toPromise().then((data:any) => {
    this.nodata_movingitems = true;
    this.http.get(this.baseUrl2 + '/employee/movingitems').toPromise().then((data: any) => {
      this.barChartdata2 = data;
      // console.log('this.barChartdata2', this.barChartdata2);
      if (data['data'].length > 0) {
        this.nodata_movingitems = false;
      }
      this.FastItemsCount = this.barChartdata2.data[0].FastItemsCount;
      this.SlowItemsCount = this.barChartdata2.data[0].SlowItemsCount;
      this.NotMovingItemsCount = this.barChartdata2.data[0].NotMovingItemsCount;


      this.xpieValues2 = ["Slow Moving", "Fast Moving", "Non Moving"];
      this.ypieValues2 = [this.SlowItemsCount, this.FastItemsCount, this.NotMovingItemsCount];
      this.barpieColors = [
        "#ff7ca3",
        "#ffb572",
        "#65b0f6"
      ];


      // this.pieChart.data.datasets = [{
      //   labels: this.xpieValues2,
      //   backgroundColor: this.barpieColors,
      //       data: this.ypieValues2
      //   // data: [this.Lead, this.Need, this.Quotation, this.Negotiation, this.Order],
      //   // backgroundColor: '#95B5FF',
      //   // borderColor: '#95B5FF',
      //   // tension: 0.4,
      // }];
      // this.pieChart.update();

      var pieChart = new Chart("pieChart", {
        type: "pie",
        data: {
          labels: this.xpieValues2,
          datasets: [{
            backgroundColor: this.barpieColors,
            data: this.ypieValues2
          }]
        },
        plugins: [ChartDataLabels],
        options: {
          events: [],
          plugins: {
            legend: {
              display: false
            },
            datalabels: {
              display: true,
              formatter: (value) => {
                return value + '%';
              },
              align: 'center',
              //  backgroundColor: 'white',
              //  borderRadius: 100,
              padding: 10,
              color: '#fff',

            }
          },
          // title: {
          //   display: true,
          //   text: "World Wide Wine Production 2018"
          // }
        }
      });
    });

  }

  shownot() {
    $(".showNoti").show();
  }



}
