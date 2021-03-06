import { Component, ViewChild, ElementRef, Renderer2, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { SearchService } from './search.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Have We Worked Together?';

  callPhone(val:string): void { //here:
    alert(val)
  }

  // // @ViewChild('hello', { static: false }) navbar!: ElementRef;
  @ViewChild('theNavbar') navbar!: ElementRef;
  @ViewChild('navbarOffset') navbarOffset!: ElementRef;
  

  // // constructor(private el: ElementRef) {
  // constructor(private navbarOffset: ElementRef, private navbar: ElementRef, private renderer: Renderer2) {
    constructor(
      private renderer: Renderer2,
      private searchService: SearchService,
      private router: Router
      ) {
  // constructor() {
  //   console.log("i'm in APPPPPPPPP");

  //   console.log("navbar is")
  //   console.log(this.navbar)
  // this.renderer.setStyle(this.navbarOffset.nativeElement, 'background-color', 'red');
  }

  ngAfterViewInit() {
    console.log("i'm in APPP 2");
    console.log(this.navbar)
    console.log(this.navbar.nativeElement.clientHeight)

    this.resizeMe()
  }

  resizeMe() {
    console.log("i'm in APPP 2");
    console.log(this.navbar)
    console.log(this.navbar.nativeElement.clientHeight)

    let currentHeight = this.navbar.nativeElement.clientHeight
    this.renderer.setStyle(this.navbarOffset.nativeElement, 'height', currentHeight+20);
  }

  ngAfterViewChecked() {
   }

  // ngOnInit() {
  //   this.navbarOffset.nativeElement.style.backgroundColor = 'red';
  //   this.renderer.setStyle(this.navbarOffset.nativeElement, 'background-color', 'red');
  // }

  @HostListener('window:resize') 
    onResize() {
      this.resizeMe()

  }

    getActors() {
      // this.searchService.getActors()
      //   .subscribe(actors => this.actors = actors);

        // this.router.navigateByUrl('/actor_search');

        this.router.navigateByUrl(
          this.router.createUrlTree(
            // ['actor_search'], {queryParams: {"query": "sana"}}
            ['search'], {queryParams: {"query": "sana", "type": "actor"}}
          )
        );
    }

    getTitles() {
      
    }
}
