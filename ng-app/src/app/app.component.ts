import { query } from '@angular/animations';
import { Component, ViewChild, ElementRef, Renderer2, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { SearchService } from './search.service';
import { baseUrl } from './base-url';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Have We Worked Together?';
  routeSegment = "";
  homepage:string = baseUrl + "/";

  @ViewChild('theNavbar') navbar!: ElementRef;
  @ViewChild('navbarOffset') navbarOffset!: ElementRef;
  @ViewChild('searchTerm') searchTerm!: HTMLInputElement;
  

    constructor(
      private renderer: Renderer2,
      private searchService: SearchService,
      private router: Router,
      private http: HttpClient
    ) {
  
        // so components can be updated when a different param is used
        this.router.routeReuseStrategy.shouldReuseRoute = function () {
          return false;
        };

  }

  ngOnInit() {}

  ngAfterViewInit() {

    this.resizeMe()
  }

  ngAfterContentChecked(): void{
    this.routeSegment = this.router.routerState.snapshot.url;
    this.routeSegment = this.routeSegment.split("/")[1]
  }

  resizeMe() {

    let currentHeight = this.navbar.nativeElement.clientHeight
    this.renderer.setStyle(this.navbarOffset.nativeElement, 'height', currentHeight+20);
  }

  @HostListener('window:resize') 
    onResize() {
      this.resizeMe()

  }

    getActors(searchTerm: string) {

        this.router.navigateByUrl(
          this.router.createUrlTree(

            ['search'], {queryParams: {"query": searchTerm, "type": "actor"}}
          )
        );
    }

    getTitles(searchTerm: string) {
      this.router.navigateByUrl(
        this.router.createUrlTree(

          ['search'], {queryParams: {"query": searchTerm, "type": "title"}}
        )
      );
    }
}
