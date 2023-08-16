<template>
  <div :class="[$style['mission-leg-wrapper']]">
    <div :class="[$style['mission-leg-wrapper__content']]">
      <AirportLocationAutocomplete
        v-model="missionFormModel.legs[legIndex].departure_location"
        :errors="errors?.departure_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Departure Airport:"
        @update:model-value="onChangeDepartureLocation"
      />
      <div class="flex flex-col mb-4 lg:mb-0">
        <ULabel required label-text="Departure Date:" />
        <UCalendar
          v-model="missionFormModel.legs[legIndex].departure_datetime"
          :is-validation-dirty="isValidationDirty"
          :errors="errors?.departure_datetime"
          :min-date="computedMinimumDepartureDate"
          :min-time="computedMinimumDepartureTime"
          :max-time="{ hours: 23, minutes: 59 }"
          :start-time="startDepartureTime"
          ignore-time-validation
          required
          @update:model-value="onChangeDepartureTime"
        />
      </div>
      <AirportLocationAutocomplete
        v-model="missionFormModel.legs[legIndex].arrival_location"
        :errors="errors?.arrival_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Destination Airport:"
        @update:model-value="onChangeArrivalLocation"
      />
      <div class="flex flex-col mb-4 lg:mb-0">
        <ULabel required label-text="Arrival Date:" />
        <UCalendar
          v-model="missionFormModel.legs[legIndex].arrival_datetime"
          :is-validation-dirty="isValidationDirty"
          :errors="errors?.arrival_datetime"
          :min-date="missionFormModel.legs[legIndex].departure_datetime"
          :min-time="computedMinimumArrivalTime"
          :max-time="{ hours: 23, minutes: 59 }"
          ignore-time-validation
          required
          @update:model-value="onChangeArrivalTime"
        />
      </div>
      <UInputWrapper
        v-model="missionFormModel.legs[legIndex].callsign_override"
        :errors="errors?.callsign_override"
        :is-validation-dirty="isValidationDirty"
        label-text="Callsign (if different):"
      />
      <UInputWrapper
        v-model="missionFormModel.legs[legIndex].pob_crew"
        required
        type="number"
        :is-validation-dirty="isValidationDirty"
        label-text="Crew:"
        :errors="errors?.pob_crew"
      />
    </div>
  </div>
  <div class="flex mb-[18px]">
    <div class="flex px-[1.5rem] mt-[6px] gap-[1.5rem] w-full">
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper
            v-model="passengersCheckbox"
            label-text="Passengers?"
            @update:model-value="onHandleCheckBox($event, 'pob_pax')"
          />
          <UInputWrapper
            v-model="passengersQuantityComputed"
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.pob_pax"
            :disabled="!passengersCheckbox"
          />
        </div>
      </div>
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper
            v-model="cargoCheckbox"
            label-text="Cargo?"
            @update:model-value="onHandleCheckBox($event, 'cob_lbs')"
          />
          <UInputWrapper
            v-model="cargoQuantityComputed"
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.cob_lbs"
            :disabled="!cargoCheckbox"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, nextTick, onMounted, PropType, ref, watch } from 'vue'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import { ErrorObject } from '@vuelidate/core'
import ULabel from '@/components/ui/form/ULabel.vue'
import AirportLocationAutocomplete from '@/components/autocomplete/AirportLocationAutocomplete.vue'
import { getMissionId } from '@/helpers'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import UCalendar from '@/components/ui/form/UCalendar.vue'
import type { ILegService, IMissionLegFormStructure } from '@/types/mission/mission.types'
import { missionLegServiceDefaults } from '@/constants/mission.constants'

const props = defineProps({
  legIndex: {
    type: Number,
    default: 0
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => ({})
  }
})

const missionFormStore = useMissionFormStore()
const missionsReferenceStore = useMissionReferenceStore()

const { selectedDestinationAirportsLeg, passengerService, cargoService } =
  storeToRefs(missionsReferenceStore)
const { formModel: missionFormModel } = storeToRefs(missionFormStore)

const computedMinimumDepartureDate = computed(() => {
  return props.legIndex === 0
    ? null
    : missionFormModel.value?.legs?.[props.legIndex - 1].arrival_datetime
})

const computedMinimumDepartureTime = computed(() => {
  const getLeg = (index) => missionFormModel.value?.legs?.[index]
  const departureDate = new Date(getLeg(props.legIndex)?.departure_datetime).setHours(0, 0, 0, 0)
  const arrivalDate = new Date(getLeg(props.legIndex - 1)?.arrival_datetime).setHours(0, 0, 0, 0)

  const [hours, minutes] = [
    new Date(getLeg(props.legIndex - 1)?.arrival_datetime)?.getHours(),
    new Date(getLeg(props.legIndex - 1)?.arrival_datetime)?.getMinutes()
  ]
  return props.legIndex === 0 || departureDate !== arrivalDate ? null : { hours, minutes }
})

const computedMinimumArrivalTime = computed(() => {
  const getLeg = (index) => missionFormModel.value?.legs?.[index]
  const departureDate = new Date(getLeg(props.legIndex)?.departure_datetime).setHours(0, 0, 0, 0)
  const arrivalDate = new Date(getLeg(props.legIndex)?.arrival_datetime).setHours(0, 0, 0, 0)

  const [hours, minutes] = [
    new Date(getLeg(props.legIndex)?.departure_datetime).getHours(),
    new Date(getLeg(props.legIndex)?.departure_datetime).getMinutes()
  ]
  return departureDate !== arrivalDate ? null : { hours, minutes }
})

const isServiceSelected = (serviceId?: string): boolean => {
  if (!serviceId) return false
  const prevLeg: IMissionLegFormStructure = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg: IMissionLegFormStructure = missionFormModel.value?.legs?.[props.legIndex]

  const isSelectedInPrevLeg = !!prevLeg?.servicing?.services?.find(
    (service) => service?.service === serviceId
  )?.on_departure
  const isSelectedInCurrentLeg = !!currentLeg?.servicing?.services?.find(
    (service) => service?.service === serviceId
  )?.on_arrival

  return isSelectedInPrevLeg || isSelectedInCurrentLeg
}

const passengersCheckbox = computed({
  get: () => {
    const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
    return (
      isServiceSelected(passengerService.value?.id) ||
      (currentLeg?.pob_pax !== null && currentLeg?.pob_pax >= 0)
    )
  },
  set: (value) => {
    if (!value) missionFormModel.value.legs[props.legIndex].pob_pax = null
    return value
  }
})

const passengersQuantityComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.pob_pax,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) return (leg.pob_pax = 0)
    leg.pob_pax = value
  }
})
const cargoCheckbox = computed({
  get: () => {
    const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
    return (
      isServiceSelected(cargoService.value?.id) ||
      (currentLeg?.cob_lbs !== null && currentLeg?.cob_lbs >= 0)
    )
  },
  set: (value) => {
    if (!value) missionFormModel.value.legs[props.legIndex].cob_lbs = null
    return value
  }
})

const cargoQuantityComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.cob_lbs,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) return (leg.cob_lbs = 0)
    leg.cob_lbs = value
  }
})

const isLastLeg = computed(() => {
  return props.legIndex === missionFormModel.value?.legs?.length - 1
})
const isFirstLeg = computed(() => {
  return props.legIndex === 0
})
const startDepartureTime = computed(() => {
  const prevLeg = missionFormModel.value.legs?.[props.legIndex - 1]
  const [hours, minutes] = [
    new Date(prevLeg?.arrival_datetime).getHours(),
    new Date(prevLeg?.arrival_datetime).getMinutes()
  ]
  return prevLeg?.arrival_datetime ? { hours, minutes } : null
})
/** function handles leg Cargo & Passenger checkbox handling
 * @param flag - checkbox state
 * @param property - dependant on checkbox leg property
 * */
const onHandleCheckBox = (
  flag: boolean,
  property: keyof Pick<IMissionLegFormStructure, 'pob_pax' | 'cob_lbs'>
) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  onHandleLegServicing(
    flag,
    property === 'pob_pax' ? passengerService.value.id : cargoService.value.id
  )
  currLeg[property] = flag ? 0 : null
}

/** function handles leg additional servicing dependant on passenger & cargo checkboxes
 * @param flag - checkbox state
 * @param service - dependant service id (passenger_handling / cargo_handling) get from reference store
 */
const onHandleLegServicing = (flag: boolean, service?: string) => {
  // Do not handle if service is missing
  if (!service) return
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  const handleService = (
    leg: IMissionLegFormStructure,
    servicingType: 'on_departure' | 'on_arrival'
  ) => {
    if (!leg.servicing?.services) return
    const serviceIndex = (leg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === service
    )
    const oppositeServicingType = servicingType === 'on_departure' ? 'on_arrival' : 'on_departure'
    // Add service if it is not present
    if (serviceIndex < 0 && flag) {
      return leg.servicing.services.push({
        ...missionLegServiceDefaults(service),
        [servicingType]: true
      })
    }
    // Remove service if not used
    if (!leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] && !flag) {
      return leg.servicing.services.splice(serviceIndex, 1)
    }
    // Update service flag
    return (leg.servicing.services[serviceIndex] = {
      ...(leg.servicing.services[serviceIndex] as ILegService),
      [servicingType]: flag
    })
  }

  if (prevLeg?.arrival_aml_service && prevLeg?.servicing && prevLeg?.servicing?.services) {
    handleService(prevLeg, 'on_departure')
  }
  if (currentLeg?.arrival_aml_service && currentLeg?.servicing && currentLeg?.servicing?.services) {
    handleService(currentLeg, 'on_arrival')
  }
}

/** function adds automatical services based on cargo & passenger checkboxes
 */
const handleAutomaticalServices = () => {
  const currentLeg: IMissionLegFormStructure = missionFormModel.value?.legs?.[props.legIndex]
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]

  const addOrUpdateService = (serviceId: string, servicingType: 'on_departure' | 'on_arrival') => {
    if (!currentLeg.servicing?.services) return

    const serviceIndex = (currentLeg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === serviceId
    )
    serviceIndex > -1
      ? (currentLeg.servicing.services[serviceIndex] = {
          ...currentLeg.servicing.services[serviceIndex],
          [servicingType]: true
        } as ILegService)
      : currentLeg.servicing?.services?.push({
          ...missionLegServiceDefaults(serviceId),
          [servicingType]: true
        })
  }
  if (currentLeg?.cob_lbs !== null) {
    addOrUpdateService(cargoService.value.id, 'on_arrival')
  }
  if (currentLeg?.pob_pax !== null) {
    addOrUpdateService(passengerService.value.id, 'on_arrival')
  }
  if (nextLeg?.cob_lbs !== null) {
    addOrUpdateService(cargoService.value.id, 'on_departure')
  }
  if (nextLeg?.pob_pax !== null) {
    addOrUpdateService(passengerService.value.id, 'on_departure')
  }
}

watch(
  () => missionFormModel.value?.legs?.[props.legIndex]?.arrival_aml_service,
  (isAmlServiceSelected) => {
    if (isAmlServiceSelected) {
      handleAutomaticalServices()
    }
  }
)
const onChangeDepartureLocation = (airportId: number) => {
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  if (prevLeg && prevLeg.arrival_location !== airportId) {
    prevLeg.arrival_location = airportId
  }
  getMissionId() && !isFirstLeg.value && resetFuelingSection(props.legIndex - 1)
}
const onChangeArrivalLocation = (airport: number) => {
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]
  if (nextLeg) {
    nextLeg.departure_location = airport
  }
  getMissionId() && !isLastLeg.value && resetFuelingSection(props.legIndex)
}
const onChangeDepartureTime = async (event) => {
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  await nextTick()
  if (event && !currentLeg.arrival_datetime) {
    currentLeg.arrival_datetime = event
  }
}
const onChangeArrivalTime = async (event) => {
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]
  const getLeg = (index) => missionFormModel.value?.legs?.[index]
  const departureDate = new Date(getLeg(props.legIndex + 1)?.departure_datetime).getTime()
  const arrivalDate = new Date(getLeg(props.legIndex)?.arrival_datetime).getTime()

  if (event && departureDate <= arrivalDate && nextLeg?.departure_datetime) {
    nextLeg.departure_datetime = event
  }
}

const resetFuelingSection = (index) => {
  if (missionFormModel.value.legs[index]) {
    missionFormModel.value.legs[index].arrival_aml_service = false
    delete missionFormModel.value.legs[index].servicing
  }
}

watch(
  () => missionFormModel.value.legs[props.legIndex]?.arrival_location,
  (location) => {
    if (location?.id) selectedDestinationAirportsLeg.value[props.legIndex] = location
  }
)
</script>

<style lang="scss" module>
.mission-leg-wrapper {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem];

  &__content {
    @apply grid px-6 gap-x-[1.5rem] gap-y-[2.5px] mt-4  grid-cols-1 lg:grid-cols-2 font-medium text-[1.25rem] text-grey-900;
  }
}
</style>
