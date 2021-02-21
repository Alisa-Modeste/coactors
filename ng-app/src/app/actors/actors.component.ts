import { ActorService } from '../actor.service';
import { Actor } from '../actor';

import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-actors',
  templateUrl: './actors.component.html',
  styleUrls: ['./actors.component.css']
})
export class ActorsComponent implements OnInit {

  // actors = ACTORS;
  actors?: Actor[];
  // actors: Actor[] | undefined; //option 2: and 'undefined' type to property 'actors'
  // actors!: Actor[]; //option 2: add definite assignment assertion to perperty 'actors: Actorr[];'
  // actors: Actor[] = []; //option 1: add initializer to peroperty 'actors'
  selectedActor?: Actor;
  onSelect(actor: Actor): void {
    this.selectedActor = actor;
  }
  
  constructor(private actorService: ActorService) { }

  // getActors(): void {
  //   this.actors = this.actorService.getActors();
  // }

  getActors(): void {
    this.actorService.getActors()
        .subscribe(actors => this.actors = actors);
  }

  ngOnInit(): void {
    this.getActors();
  }

}
