# Commits

Настоятельно рекомендую коммитить маленькими частями по сделанным мини-фичам

> Пример:\
> Вы делаете авторизацию. Отдельный коммит на модели и миграции, на вьюхи с шаблонами

---

## Commit message

Коммиты пишем в стиле [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)

> Примеры:
>
> - feat(analytics page): add new graphs for drivers segment
> - build(image plugin): add plugin for image compression
> - fix: fix window reload bug

---

## Git flow

Есть статические ветки: `master` и `development`\
Для других веток есть 2 типа названий:

- `feature/*` - фича-ветки
- `hotfix/*` - ветка для срочных фиксов

Новые feature-ветки откалываются от и мерджатся в `development`
Новые hotfix-ветки откалываются от и мерджатся в `master`

В название ветки после слеша добавляем айдишник таски, в коммит месседж - айдишник и статус

> Примеры:
>
> - feature/#861mhc4nj_docs
> - feat: add docs #861mhc4nj[completed]

MR на hotfix не нуждается в аппруве
MR на фичу нуждается в аппруве хотя бы 1 человека
