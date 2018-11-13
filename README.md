# Inventory solution for the GildedRose
### Helpful links
[Original problem statement](./ProblemStatement.md)
[Questions from the problem statement](./Q-n-A.md)
License [MIT License](License)
[Questions from the problem statement](./Q-n-A.md)

##Design
### DB
Chose tinydb - simple, sschemaless and lightweight. This all means that it'll be easy to change the schema as the 
requirements change. And they will.

#### Initial layout
|field name ->   | Name       | quality             | sell-by                      | degradation                     | comments             | category|
|----------------|------------|---------------------|------------------------------|---------------------------------|----------------------|----------------------------------------|
|description     | item name  | value, like bucks $ | Number of days to expiration | how fast to degrade the quality | comments on the item | category of item – normal, legendary
|datatype        | string     | int                 | int                          | float                           | string or memo       | String|
|min             | 1 character| 80                  | 0 {today}                    | 0 {none}                        | None                 | enumerated type?|
|max             | 256 chars  | maxint              |                              |                                 | 1024 chars           | | 
|comments and rules | none| if a legendary item, value is 80. If a normal item, value max is 50 | If legendary, doesn't apply. | If legendary, 0. Negative for reverse degradation? Default is 1. Looks like we need a functor/function reference | additional notes for this item | allow for expansion|
|                |            |                     |                              | generally equal to quality/sell-by | not used by UI, may be used for popup and should be gated by a UI config switch | Might be able to use this to trigger reverse degradation, like cheese|





### Phases
#### 1). Data import, save to DB
#### data services - be able to serve data
  * List all
  * List trash
  * Increment day
  * Search by name
#### Presentation
Develop nice UI
  * All of the above plus
    * sort by column
    * filter (e.g. Legendary only, What HAS to be sold tomorrow)

### nice to haves - 
  * service discovery. Considering the forum, will do this without using a framework (e.g. Consul)
  * Automation (Ansible)
  * Filtering (e.g. show only Legendary)