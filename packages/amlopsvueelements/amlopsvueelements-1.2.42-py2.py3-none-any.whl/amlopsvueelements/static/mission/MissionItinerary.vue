<template>
  <div :class="$style['mission-itinerary']">
    <div :class="$style['mission-itinerary__items']">
      <div
        v-for="(leg, index) in formData.legs as IMissionLeg[]"
        :key="index"
        :class="$style['mission-itinerary__item']"
      >
        <div class="flex items-center w-full">
          <div class="w-full">
            <UFormWrapper
              :is-loading="isLoading || isCancelingMissionLeg"
              :class="$style['mission-itinerary__wrapper']"
            >
              <template #header>
                <div :class="$style['mission-itinerary__header']">
                  <div :class="$style['mission-itinerary__title']">
                    <h1>Mission Leg: {{ leg.sequence_id }}</h1>
                  </div>
                  <UButton
                    v-if="leg.sequence_id !== 1 && formData?.legs?.length >= 3"
                    class="bg-transparent p-0"
                    :class="$style['mission-itinerary__delete']"
                    @click="onDeleteLeg(leg, index)"
                  >
                    <img :src="getImageUrl('assets/icons/delete.png')" alt="delete" />
                  </UButton>
                </div>
              </template>
              <template #content>
                <MissionLegWrapper
                  :is-validation-dirty="validationInfo?.$dirty"
                  :leg-index="index"
                  :errors="validationInfo?.legs?.$each?.$response?.$errors?.[index] as Record<string, ErrorObject[]>"
                />
              </template>
            </UFormWrapper>
            <FuelingSection
              v-if="index !== formData.legs?.length - 1"
              class="mission-itinerary__show-mobile-aml overflow-hidden transition-all duration-500"
              :class="localControls[index] ? 'max-h-screen h-full mt-4' : 'max-h-0'"
              :validation-info="validationInfo"
              :is-loading="isLoading"
              :leg="leg"
              :index="index"
            />
            <div :class="[$style['add-new-mission']]" @click="createMissionLeg(leg.sequence_id)">
              <span :class="$style['add-new-mission__line']" />
              <span :class="$style['add-new-mission__sign']">+</span>
            </div>
          </div>
          <div
            class="flex lg:hidden"
            :class="[
              $style['mission-itinerary__show-aml'],
              $style['show-aml'],
              index !== formData.legs?.length - 1 ? 'visible' : 'invisible'
            ]"
          >
            <button
              :class="[
                $style['show-aml__btn'],
                localControls[index] ? '!bg-confetti-500' : '!bg-grey-900'
              ]"
              @click="localControls[index] = !localControls[index]"
            >
              <img :src="getImageUrl(`assets/icons/fuel.png`)" alt="fuel" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="my-auto flex flex-col lg:w-[45%] gap-[28px]">
      <template v-for="(leg, index) in formData.legs as IMissionLeg[]" :key="index">
        <FuelingSection
          v-if="index !== formData.legs?.length - 1"
          class="hidden lg:flex"
          :validation-info="validationInfo"
          :is-loading="isLoading"
          :leg="leg"
          :index="index"
        />
      </template>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { onBeforeMount, onMounted, onUnmounted, PropType, ref, watch } from 'vue'
import UFormWrapper from '@/components/ui/wrappers/UFormWrapper.vue'
import MissionLegWrapper from '@/components/forms/MissionLegWrapper.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import type { IMissionLeg } from '@/types/mission/mission.types'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import { BaseValidation, ErrorObject } from '@vuelidate/core'
import { getImageUrl } from '@/helpers'
import UButton from '@/components/ui/form/UButton.vue'
import { useMission } from '@/composables/mission/useMission'
import { useMissionStore } from '@/stores/useMissionStore'
import FuelingSection from '@/components/forms/FuelingSection.vue'

defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => {}
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  }
})

const missionFormStore = useMissionFormStore()
const missionStore = useMissionStore()
const { createMissionLeg, onDeleteMissionLeg } = useMission()
const { initiateReferenceStore } = useMissionReferenceStore()
const { formModel: formData } = storeToRefs(missionFormStore)
const { isCancelingMissionLeg } = storeToRefs(missionStore)

const marginTop = ref(0)
const localControls = ref([])

const onDeleteLeg = async (leg: IMissionLeg, index: number) => {
  const [departureTinyCode, arrivalTinyCode] = [
    leg?.departure_location?.tiny_repr,
    leg?.arrival_location?.tiny_repr
  ]
  const deletionLegNumberText = `Please confirm deletion of flight leg ${leg.sequence_id}`
  const deletionCodeText =
    departureTinyCode && arrivalTinyCode
      ? `(${departureTinyCode || ''} > ${arrivalTinyCode || ''})`
      : ''
  const deletionText = `${deletionLegNumberText} ${deletionCodeText}`
  const isConfirmed = await onDeleteMissionLeg(leg, deletionText)
  if (isConfirmed) await changeDepartureAirportOnDelete(index)
}
const changeDepartureAirportOnDelete = (index) => {
  const currLeg = formData.value?.legs?.[index]
  const prevLeg = formData.value?.legs?.[index - 1]
  if (currLeg && prevLeg) {
    currLeg.departure_location = prevLeg.arrival_location
  }
}
const onResizeWindow = () => {
  if (window.innerWidth > 1024) {
    localControls.value = new Array(formData.value.legs?.length).fill(false)
  }
}
watch(
  () => formData.value.legs?.[0].servicing?.services?.length,
  (newValue, oldValue) => {
    if (newValue > oldValue) {
      if (marginTop.value < 0) return
      marginTop.value = marginTop.value - 33.5
    } else {
      if (marginTop.value > 251.25) return
      marginTop.value = marginTop.value + 33.5
    }
  },
  { immediate: true }
)

onBeforeMount(async () => {
  await initiateReferenceStore()
})
onMounted(() => {
  const arrayLength = formData.value.legs?.length
  localControls.value = new Array(arrayLength).fill(false)
  window.addEventListener('resize', onResizeWindow)
})
onUnmounted(() => {
  window.removeEventListener('resize', onResizeWindow)
})
</script>
<style lang="scss">
.mission-itinerary__aml {
  .ops-form-wrapper__header {
    @apply hidden;
  }
}
</style>
<style lang="scss" module>
.mission-itinerary {
  @apply flex flex-col lg:gap-x-6 w-full sm:flex-row pb-4 relative;
  &__header {
    @apply flex items-center w-full justify-between;
  }
  &__line {
    @apply mx-[1.5rem];
  }
  &__title {
    @apply rounded-md flex items-center;
    img {
      @apply h-4 w-4 mr-1;
      filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(118deg) brightness(107%) contrast(101%);
    }
  }
  &__delete {
    img {
      @apply h-6 w-6;
      filter: invert(23%) sepia(85%) saturate(2552%) hue-rotate(330deg) brightness(87%)
        contrast(103%);
    }
  }
  &__items {
    @apply flex flex-col w-full lg:w-[55%] gap-0;
  }
  &__aml {
    @apply flex flex-col  w-full gap-[1.625rem];
    .ops-form-wrapper__header {
      height: 20px;
      background: red !important;
    }
  }
  .show-aml {
    @apply justify-center mr-4 shrink-0 ml-4 lg:ml-0;
    &__btn {
      @apply p-4 rounded-full transition-all #{!important};
      img {
        @apply w-10;
        filter: invert(100%) sepia(100%) saturate(14%) hue-rotate(212deg) brightness(104%)
          contrast(104%);
      }
      &:hover {
        @apply scale-[1.04];
      }
    }
  }
  &__item {
    @apply relative lg:w-full;
    .add-new-mission {
      @apply transition-all opacity-0 duration-500 invisible mb-2;
    }
    &:hover {
      .add-new-mission {
        @apply opacity-100 mt-[0.3rem] transition-all duration-500 visible;
      }
    }
  }
  &__show-mobile-aml {
    @apply min-w-[30rem] w-full mt-4 bg-white block #{!important};
  }
  &__wrapper {
    @apply relative w-full;
  }
  .add-new-mission {
    @apply transform duration-500 relative transition-all cursor-pointer z-[1];
    &__line {
      @apply bg-grey-900 absolute top-[53%] h-[1px] w-full block;
    }
    &__sign {
      @apply w-5 h-5 text-grey-800 flex text-[0.96875rem] justify-center rounded-full bg-white mx-auto items-center relative;
    }
  }
}
</style>
